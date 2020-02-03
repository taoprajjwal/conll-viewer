from PIL import ImageDraw, Image, ImageFont
import random
import os
import pathlib

class Fonts:
    """
    STORING THE LOCATION FOR FONT FILES
    """
    DEFAULTFONT=str(os.path.join(os.path.join(pathlib.Path(__file__).parent.absolute(),"fonts"),"Exo-Medium.otf"))
    FNAMEFONT=str(os.path.join(os.path.join(pathlib.Path(__file__).parent.absolute(),"fonts"),"PRIMERB.ttf"))
    ARGFONT=str(os.path.join(os.path.join(pathlib.Path(__file__).parent.absolute(),"fonts"),"BabelSans.ttf"))

class Word():
    """
    Word class representing each line in the conll file
    """
    def __init__(self, line):
        """
        :param line: the line representing the word and its properties.
        """
        self.contents = line.split()
        self.frame = None
        self.lex_unit = None
        try:
            self.form = self.contents[1]
            self.sentence_id = int(self.contents[0])
            self.tag = "O"
            self.arg = None
        except:
            raise Exception("The above line is not in the valid format")

        if self.contents[-2] != "_":
            self.frame = line.split()[-2]
            self.lex_unit = line.split()[-3]

        if self.contents[-1] != "O":
            self.tag = self.contents[-1].split("-")[0]
            self.arg = self.contents[-1].split("-")[1]

    def __str__(self):
        return self.form


class GroupedWords(Word):
    """
    Words grouped together through a common tag.
    """
    def __init__(self, word_list):
        """

        :param word_list: List of Word Objects comprising the Group Object
        """
        self.frame = None
        self.words = word_list.sort(key=lambda w: w.sentence_id)
        self.arg = word_list[0].arg
        self.invalid_group = False
        self.form = ""
        for word in word_list:
            self.form += word.form + " "
            if self.arg != word.arg:
                self.invalid_group = True
            if word.frame:
                self.frame = True
                self.lex_unit = word.lex_unit
        self.form = self.form[:-1]
        self.sentence_id = min([w.sentence_id for w in word_list])

    def __str__(self):
        return self.form


class Sentence():

    def __init__(self, sentence_block):
        """
        :param sentence_block: Block of conll file representing the sentence
        """
        words = sentence_block.split("\n")
        self.words = []
        self.grouped_words = {}
        group_count = 0
        for line in words:
            w = Word(line)
            if w.frame:
                self.frame_w = w
            if w.arg:
                if w.tag == "B" or w.tag == "S":
                    group_count += 1;

                arg_list = self.grouped_words.get(group_count, [])
                arg_list.append(w)
                self.grouped_words[group_count] = arg_list

            else:
                self.words.append(w)

        for group in self.grouped_words.values():
            if group:
                gw = GroupedWords(group)
                if gw.invalid_group:
                    for word in group:
                        print(word)
                    raise Exception("Group with above words is invalid")
                self.words.append(gw)

        self.words.sort(key=lambda w: w.sentence_id)

        self.x = 10
        self.y = 50

    def get_canvas_size(self, font):
        """
        Setting up the canvas and size calculations
        :param font: PIL font object  to be used
        :return: size of the canvas
        """
        im = Image.new('RGB', (10, 10))
        size = ImageDraw.Draw(im).textsize(self.__str__(), font=font)

        return (size[0] + 5 * len(self.words), 200)

    def draw(self,def_font=Fonts.DEFAULTFONT,arg_font=Fonts.ARGFONT,frame_font=Fonts.FNAMEFONT):
        """
        :param def_font: Font for default words (non- frame non-arguments_
        :param arg_font: Fonts for arguments (non-frame but a semantic part of the sentence, also used for the lexical unit representation)
        :param frame_font: Font for representing the name of the frame at the bottom of the picture
        :return: PIL image object
        """
        font = ImageFont.truetype(def_font, 24)
        c_size = self.get_canvas_size(font)
        im = Image.new('RGB', c_size, color="white")
        d = ImageDraw.Draw(im)
        color_list = ['red', 'blue', 'brown', 'chartreuse', 'Crimson', 'orange', 'gold', 'olive', 'tan', 'tomato',
                      "IndianRed", "FireBrick", "PaleVioletRed", "DarkKhaki", "Fuchsia", "RebeccaPurple", "DarkMagenta",
                      "MediumSlateBlue", "MediumTurquoise", "CornflowerBlue"]

        for word in self.words:
            twidth, theight = d.textsize(word.form, font=font)
            lx, ly = self.x, self.y + theight + 10

            if word.frame:
                color = "green"
            elif word.arg:
                color = color_list.pop(random.randint(0, len(color_list) - 1))
            else:
                color = "black"

            d.text((self.x, self.y), word.form, font=font, fill=color)

            if word.frame:
                fm_fon = ImageFont.truetype(arg_font, 18)
                d.text((self.x, self.y - 20), word.lex_unit, font=fm_fon, fill="green")
            if word.arg:
                d.line((lx, ly, lx + twidth, ly), fill=color)
                up_fon = ImageFont.truetype(def_font, 18)
                d.text((lx + twidth / 2, ly + 10), word.arg, font=up_fon, fill=color)

            self.x += twidth + 5

        font = ImageFont.truetype(frame_font, 48)
        f_size = d.textsize(self.frame_w.frame, font=font)
        d.text((c_size[0] / 2 - f_size[0] / 2, c_size[1] - f_size[1] - 10), self.frame_w.frame, font=font, fill="red")

        return im


    def __str__(self):
        import string
        s = ""
        for word in self.words:
            if word.form[0] in string.punctuation:
                s = s[:-1] + word.form + " "
            else:
                s += word.form + " "
        return s[:-1]

    def __eq__(self, other):

        return self.__str__() == other.__str__()


class reader():
    """
    Reader class representing a Conll file
    """
    def __init__(self,file_location):
        f=open(file_location,"r").read()
        self.sentences=f.split("\n\n")[:-1]

    def get_sentences(self,limit=None):
        """
        Decompose the conll file into sentence objects
        :param limit: Number of sentences from the PIL file to read. Read sequentially
        :return: List of Sentence Objects
        """
        if limit:
            sentences=self.sentences[:limit]
        else:
            sentences=self.sentences

        sentences_l=[]
        for sentence in sentences:
            sentences_l.append(Sentence(sentence))

        return sentences_l

