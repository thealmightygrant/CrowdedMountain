from selenium import webdriver
import unittest

class HWSegCountTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_see_front_range_approximations(self):

        #Joe Snowboarder lives in Boulder, CO.  He has heard 
        #     about some fucking web app that tells him about 
        #     how many people are at each ski slope
        self.browser.get('http://localhost:8000/cdot_hw_data/')

        #He notices that the homepage tells him how that this 
        #    website will be about how big the crowds are at 
        #    the mountains and he is psyched
        assert 'Mountain Crowd Estimates' in self.browser.title

        #He is asked which group of mountains that he is 
        #    interested in straight away

        #He clicks the box indicating that he is interested 
        #    in the front range (Keystone, A Basin, Loveland)

        #The page updates and he is presented with some shitty 
        #     approximations of the HW segments that are leading 
        #     up to his favorite ron range resorts

    def test_can_see_vail_valley_approximations(self):

        #He has the option on the right to choose other areas of the range

        #He chooses the Breckenridge/Vail/Beaver Creek/Copper 
        #    Mountain area and checks out the counts
        pass

if __name__ == '__main__':
    unittest.main()
