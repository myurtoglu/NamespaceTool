import sublime
import sublime_plugin
import re


## return line as a list of strings
def get_line_from_region(view, region):
    return (view.substr(view.line(region))).split()


def is_containing_namespace(query, namespace):
    search_pattern = namespace + "::"
    return query.count(search_pattern) > 0


def append_namespace(query, namespace):
    if not is_containing_namespace(query, namespace):
        query = namespace + "::" + query
    return query


def make_using_prefix(namespace):
    return "using " + namespace + "::"


## take line in the form of a list of strings
def is_include_line(line):
    return line.count("#include") > 0


def strip_namespace(query, namespace):
    namespace_length = len(namespace) + 2
    return query[namespace_length:]


def make_using_statement(word, namespace):
    return "using " + namespace + "::" + word + ";"


## convert 'namespace::query' to 'query' format and add using statements
def refactor_to_using(edit, view, query, namespace):

    insertion_pos = 0
    query = append_namespace(query, namespace)
    stripped_query = strip_namespace(query, namespace)
    using_statement = make_using_statement(stripped_query, namespace)
    found_regions = view.find_all("\\b" + query + "\\b")

    if view.find(using_statement, 0):
        using_statements = view.find_all(make_using_prefix(namespace))
        last_using_statement_pos = using_statements[-1]
        replace_reg = view.find(query, last_using_statement_pos.b)
        while replace_reg:
            view.replace(edit, replace_reg, stripped_query)
            replace_reg = view.find(query, last_using_statement_pos.b)

    elif found_regions:
        for reg in found_regions[::-1]:
            view.replace(edit, reg, stripped_query)

        insertion_reg = view.find_all(make_using_prefix(namespace))

        if not insertion_reg:
            insertion_reg = view.find_all("#include")

        if insertion_reg:
            last_include_line = view.line(insertion_reg[-1])
            insertion_pos = last_include_line.end()
            using_statement = "\n" + using_statement

        if insertion_pos == 0:
            using_statement = using_statement[1:] + "\n"

        view.insert(edit, insertion_pos, using_statement)


## remove using statements and convert 'query' to 'namespace::query' format
def refactor_to_namespace(edit, view, query, namespace):
    query = append_namespace(query, namespace)
    stripped_query = strip_namespace(query, namespace)
    using_statement = make_using_statement(stripped_query, namespace)
    view.erase(edit, view.full_line(view.find(using_statement, 0)))
    found_regions = view.find_all("\\b" + stripped_query + "\\b")
    already_namespaced_regions = view.find_all(query)

    if found_regions:
        for reg in found_regions[::-1]:
            intersecting = False
            for a_reg in already_namespaced_regions:
                if reg.intersects(a_reg):
                    intersecting = True

            if (not intersecting and
                    not is_include_line(get_line_from_region(view, reg))):
                view.replace(edit, reg, query)


## take line in the form of a string
def is_using_line(line, namespace):
    return line.count(make_using_prefix(namespace)) > 0


## return selected word as a string
def get_query_word(view):
    selection = view.sel()[0]
    if len(selection) == 0:
        selection = view.word(selection)
    return view.substr(selection)


## return selected area as a string
def get_query_line(view):
    selection = view.sel()[0]
    if len(selection) == 0:
        selection = view.line(selection)
    return view.substr(selection)


class NamespaceToolCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        settings = sublime.load_settings('C++NamespaceTool.sublime-settings')
        namespaces = settings.get('namespaces')
        input_word = get_query_word(view)
        input_lines = get_query_line(view)
        split_input_lines = [i.lstrip().rstrip() for i in
                             list(filter(lambda x: x != '',
                                  input_lines.splitlines()))]

        no_highligt_mode = not (input_word == input_lines)
        has_using_line = False

        for namespace in namespaces:
            for line in split_input_lines:
                if is_using_line(line, namespace):
                    has_using_line = True
                    break
            if has_using_line:
                break

        if has_using_line:
            for namespace in namespaces:
                namespace_lines = list(filter(
                    lambda x: is_using_line(x, namespace), split_input_lines))

                for line in namespace_lines:
                    refactor_to_namespace(edit, view, line[6:-1], namespace)

        else:
            if no_highligt_mode:
                for namespace in namespaces:
                        refactor_to_using(edit, view, input_word, namespace)
            else:
                for line in split_input_lines:
                    for word in re.sub(r'([^\:\s\w])+', ' ', line).split():
                        for namespace in namespaces:
                            refactor_to_using(edit, view, word, namespace)

    def is_visible(self):
        fname = self.view.file_name().lower()
        settings = sublime.load_settings('C++NamespaceTool.sublime-settings')
        extensions = settings.get('filename_extensions')
        if fname:
            for extension in extensions:
                if extension.isalnum():
                    search_pattern = "\\b(\w+)\." + extension + "\\b"
                    if re.search(search_pattern, fname):
                        return True
                else:
                    if fname.count(extension) > 0:
                        return True
        return False
