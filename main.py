from databases import (alchemy_controller, 
                       config)




db = alchemy_controller.Alchemist(config.test_db)


tiles = ['35e4d824-f7da-489a-8701-edf7cf4e1ee5',
         '591affcc-8217-42a7-90c0-21b3e1bdb4e7', 
         '2efd5b28-93ba-4da2-abc3-c895077ffc93']

u = db.get_user('TEST_USER_001')
print(u.tiles)


