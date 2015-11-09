

class MyTest(object):
    @classmethod
    def setUpClass(cls):
        from stanford_parser.parser import Parser
        cls.parser = Parser()



    def testParse(self):
        str = "Vidish chem ya zanimajus po nastoyashemu. "

        print(self.parser.parseToWordsWithTag(str))


        #(tokens, tree) = self.parser.parse(str)
        #print(tree)
        #dependencies = self.parser.parseToStanfordDependencies(str)
        #tupleResult = [(dep.text, dependencies.tagForTokenStandoff(dep)) for rel, gov, dep in dependencies.dependencies]

        #print(dependencies.dependencies)
        #print(tupleResult)

        #if (tupleResult == [('det', 'girl', 'The'),
        #                               ('nsubj', 'sister', 'girl'),
        #                               ('nsubj', 'met', 'I'),
         #                              ('rcmod', 'girl', 'met'),
         #                              ('cop', 'sister', 'was'),
        #                               ('poss', 'sister', 'your')]):
        #    print (True)
        #else:
        #    print (False)

    def test(self):
        self.setUpClass()
        self.testParse()



MyTest().test()