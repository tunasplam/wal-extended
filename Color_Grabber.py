from re import findall


class Color_Grabber:

    """
    This class reads colors in from xresources and returns them in a list.
    """

    def grab_colors():
        """Summary

        Returns:
            list: list of strings representing the colors in xresources.
        """
        with open("/home/jordan/.cache/wal/colors.Xresources", 'r') as xres:
            xresources = xres.read()

        # Grab the lines with the colors.
        cols = findall(r'color[0-9]{1,2}: \#[0-9a-zA-Z]{6}', xresources)

        # Extract the color from each line.
        cols = list(map(lambda x: findall(r'#[0-9a-zA-Z]{6}', x)[0], cols))

        return cols

    def grab_colors_dict():
        """Grabs to colors from xresources and converts them to a dict

        Returns:
            dict: key: col[i] value: hex value for color i
        """

        cols_list = Color_Grabber.grab_colors()

        cols_dict = {}

        for i in range(9):
            cols_dict['col_{}'.format(i)] = cols_list[i]

        return cols_dict

    def update_colors_css():
        """
        Updates the css files that stores our color schemes. Note that there is
        a separate color file for the gtk theme since it uses an older version
        of css.
        """
        cols = Color_Grabber.grab_colors()

        # gtk css file
        template = "@define-color color{} {};"
        strs = []
        i = 0
        for col in cols:
            strs.append(template.format(i, col))
            i += 1

        text = '\n'.join(strs)
        with open("colors_gtk.css", 'w') as file:
            file.write(text)

        # now the regular css file
        template = "\t--color{}: {};"
        text = ":root {\n"
        strs = []
        i = 0
        for col in cols:
            strs.append(template.format(i, col))
            i += 1

        text += '\n'.join(strs)
        text += '\n}'

        with open("colors.css", 'w') as file:
            file.write(text)

