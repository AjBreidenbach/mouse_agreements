import pypandoc
import re


LEVEL_A = re.compile(r'\{\\pard.*\d\..*\\par\}')
LEVEL_B = re.compile(r'\{\\pard.*\\endash.*\\par\}')
LEVEL_C = re.compile(r'\{\\pard.*\\bullet.*\\par\}')

class Document:
    def __init__(self, text):
        text = pypandoc.convert_text(text, 'rtf', format='md', extra_args=['--standalone'])
        self.heading = text[0:re.search(r'.*\{\\pard', text, re.M).span()[0]]
        self.body = text[len(self.heading):]
        self.heading = self.heading.replace(r'\fswiss Helvetica;', r'\fnil ;')
        self.body = self.body.replace(r'\tx360\tab', r'\emspace ')
        self.__populate_sections__()

        self.output = self.heading + '\n' + '\n'.join(self.sections)




    def __populate_sections__(self):
        lines = self.body.split('\n')
        lev_a = 0
        lev_b = 0
        lev_c = 0

        self.sections = []

        section = []

        def push_section():
            if section:
                self.sections.append('\n'.join(section))
                section.clear()

        for line in lines:
            match = LEVEL_A.match(line)
            if match:
                push_section()
                lev_a += 1
                lev_b = 0
                lev_c = 0
                section.append(line)
                continue

            match = LEVEL_B.match(line)
            if match:
                lev_b += 1
                lev_c = 0
                section.append(line.replace(r'\endash', f'{lev_a}.{lev_b}.'))
                continue

            match = LEVEL_C.match(line)
            if match:
                lev_c += 1
                section.append(line.replace(r'\bullet', f'{lev_a}.{lev_b}.{lev_c}.'))
                continue

            self.sections.append(line)

        push_section()


import unittest

class TestDocumentOutput(unittest.TestCase):
    def test1(self):
        with open('test-cases/word-test.md') as test_file:
            document = Document(test_file.read())
        self.maxDiff = None
        self.assertEqual(
                document.output,
r'''{\rtf1\ansi\deff0{\fonttbl{\f0 \fnil ;}{\f1 Courier;}}
{\colortbl;\red255\green0\blue0;\red0\green0\blue255;}
\widowctrl\hyphauto


{\pard \ql \f0 \sa180 \li0 \fi0 \b \fs36 title\par}
{\pard \ql \f0 \sa0 \li360 \fi-360 1.\emspace  Some item\par}
{\pard \ql \f0 \sa0 \li720 \fi-360 1.1. \emspace  Some child item\par}
{\pard \ql \f0 \sa0 \li1080 \fi-360 1.1.1. \emspace  Some deeper child\sa180\sa180\par}
}

{\pard \ql \f0 \sa0 \li360 \fi-360 2.\emspace  Some item\par}
{\pard \ql \f0 \sa0 \li720 \fi-360 2.1. \emspace  Some child item\sa180\sa180\par}'''
                )
        


if __name__== '__main__':
    unittest.main()
    #with open('./test-cases/word-test.md') as test_file:
    #    document = Document(test_file.read())
    #    print(document.output)
