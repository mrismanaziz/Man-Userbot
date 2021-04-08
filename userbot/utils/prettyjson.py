# https://github.com/andy-gh/prettyjson/blob/master/prettyjson.py


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(obj, itemkey="", islast=True,
                           maxlinelength=maxlinelength - indent, indent=indent)
    return indentitems(items, indent, level=0)


def getsubitems(obj, itemkey, islast, maxlinelength, indent):
    items = []
    is_inline = True      # at first, assume we can concatenate the inner tokens into one line

    isdict = isinstance(obj, dict)
    islist = isinstance(obj, list)
    istuple = isinstance(obj, tuple)
    isbasictype = not (isdict or islist or istuple)

    maxlinelength = max(0, maxlinelength)

    # build json content as a list of strings or child lists
    if isbasictype:
        # render basic type
        keyseparator = "" if itemkey == "" else ": "
        itemseparator = "" if islast else ","
        items.append(
            itemkey +
            keyseparator +
            basictype2str(obj) +
            itemseparator)

    else:
        # render lists/dicts/tuples
        if isdict:
            opening, closing, keys = ("{", "}", iter(obj.keys()))
        elif islist:
            opening, closing, keys = ("[", "]", range(0, len(obj)))
        elif istuple:
            # tuples are converted into json arrays
            opening, closing, keys = ("[", "]", range(0, len(obj)))

        if itemkey != "":
            opening = itemkey + ": " + opening
        if not islast:
            closing += ","

        itemkey = ""
        subitems = []

        # get the list of inner tokens
        for (i, k) in enumerate(keys):
            islast_ = i == len(obj) - 1
            itemkey_ = ""
            if isdict:
                itemkey_ = basictype2str(k)
            inner, is_inner_inline = getsubitems(
                obj[k], itemkey_, islast_, maxlinelength - indent, indent)
            # inner can be a string or a list
            subitems.extend(inner)
            # if a child couldn't be rendered inline, then we are not able
            # either
            is_inline = is_inline and is_inner_inline

        # fit inner tokens into one or multiple lines, each no longer than
        # maxlinelength
        if is_inline:
            multiline = True

            # in Multi-line mode items of a list/dict/tuple can be rendered in multiple lines if they don't fit on one.
            # suitable for large lists holding data that's not manually
            # editable.

            # in Single-line mode items are rendered inline if all fit in one line, otherwise each is rendered in a separate line.
            # suitable for smaller lists or dicts where manual editing of
            # individual items is preferred.

            # this logic may need to be customized based on visualization
            # requirements:
            if (isdict):
                multiline = False
            if (islist):
                multiline = True

            if (multiline):
                lines = []
                current_line = ""

                for (i, item) in enumerate(subitems):
                    item_text = item
                    if i < len(inner) - 1:
                        item_text = item + ","

                    if len(current_line) > 0:
                        try_inline = current_line + " " + item_text
                    else:
                        try_inline = item_text

                    if (len(try_inline) > maxlinelength):
                        # push the current line to the list if maxlinelength is
                        # reached
                        if len(current_line) > 0:
                            lines.append(current_line)
                        current_line = item_text
                    else:
                        # keep fitting all to one line if still below
                        # maxlinelength
                        current_line = try_inline

                    # Push the remainder of the content if end of list is
                    # reached
                    if (i == len(subitems) - 1):
                        lines.append(current_line)

                subitems = lines
                if len(subitems) > 1:
                    is_inline = False
            else:  # single-line mode
                totallength = len(subitems) - 1   # spaces between items
                for item in subitems:
                    totallength += len(item)
                if (totallength <= maxlinelength):
                    str = ""
                    for item in subitems:
                        str += item + " "  # insert space between items, comma is already there
                    # wrap concatenated content in a new list
                    subitems = [str.strip()]
                else:
                    is_inline = False

        # attempt to render the outer brackets + inner tokens in one line
        if is_inline:
            item_text = ""
            if len(subitems) > 0:
                item_text = subitems[0]
            if len(opening) + len(item_text) + len(closing) <= maxlinelength:
                items.append(opening + item_text + closing)
            else:
                is_inline = False

        # if inner tokens are rendered in multiple lines already, then the
        # outer brackets remain in separate lines
        if not is_inline:
            items.append(opening)       # opening brackets
            # Append children to parent list as a nested list
            items.append(subitems)
            items.append(closing)       # closing brackets

    return items, is_inline


def basictype2str(obj):
    if isinstance(obj, str):
        strobj = "\"" + str(obj) + "\""
    elif isinstance(obj, bool):
        strobj = {True: "true", False: "false"}[obj]
    else:
        strobj = str(obj)
    return strobj


def indentitems(items, indent, level):
    """Recursively traverses the list of json lines, adds indentation based on the current depth"""
    res = ""
    indentstr = " " * (indent * level)
    for (i, item) in enumerate(items):
        if isinstance(item, list):
            res += indentitems(item, indent, level + 1)
        else:
            islast = (i == len(items) - 1)
            # no new line character after the last rendered line
            if level == 0 and islast:
                res += indentstr + item
            else:
                res += indentstr + item + "\n"
    return res
