import unittest
from con import contact
from actions import getting_contacts_notification


class ContentMailTestCase(unittest.TestCase):
    def setUp(self):
        contact.insert_one({
            'email': 'email_lower@mail.com',
            'rules': 'menor',
            'value': float(1500),
            'sent': False
        })
        contact.insert_one({
            'email': 'email_upper@mail.com',
            'rules': 'maior',
            'value': float(1500),
            'sent': False
        })

    def test_lower(self):
        all_contacts = getting_contacts_notification({'last': 1400})
        self.assertEqual(len(all_contacts), 1)

    def test_upper(self):
        all_contacts = getting_contacts_notification({'last': 1600})
        self.assertEqual(len(all_contacts), 1)

    def test_upper_and_lower(self):
        contact.insert_one({
            'email': 'email@mail.com',
            'rules': 'menor',
            'value': float(1700),
            'sent': False
        })
        all_contacts = getting_contacts_notification({'last': 1600})
        self.assertEqual(len(all_contacts), 2)

    def test_no_resend_mail(self):
        contact.update_many({'sent': False}, {'$set': {'sent': True}})
        all_contacts = getting_contacts_notification({'last': 1600})
        self.assertEqual(len(all_contacts), 0)

    def tearDown(self):
        contact.delete_many({})


if __name__ == '__main__':
    unittest.main()
