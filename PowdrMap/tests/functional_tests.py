from selenium import webdriver
import unittest

class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    
    def test_can_get_current_skier_estimate(self):
        
        self.browser.get('http://localhost:8000')
        # Joe has heard about a cool new online mountain app. He goes
        # to check out its homepage

        self.assertIn('Mountain Crowd Estimates', self.browser.title)
        # He notices the page title and header mention Mountain Crowd estimation

        self.fail('Finish writing this test!!!')
        # He is invited to pick a Colorado mountain right away

        # The page transitions to one concerning his favorite mountain with 
        # an estimate of the number of people at that mountain, today, tomorrow,
        # and next weekend including the expected amount of snow coming in

        # He can click on each of these dates and an enlarged estimate is shown
        # with options to see the current estimate of people at each region of 
        # of the mountain he is interested in, the number of people expected to be
        # at each skill level, and the expected drive time to and from throughout the day

        # At the bottom (or top) of the page, there is still an option for Joe
        # to check out other close by mountains, so he does

        # Each time he clicks a new mountain the page updates with the "skier"
        # traffic information for that mountain.

        # Satisfied, he packs up and heads to the mountains or sits at home and cries

if __name__ == '__main__':
    unittest.main()
