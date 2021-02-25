import os
import sys
import secrets
import unittest

from models import *
from main import save_picture


class TestDB(unittest.TestCase):

    def setUp(self):
        self.raw_password = "TestPassword123"
        self.password = bcrypt.generate_password_hash(self.raw_password).decode('utf-8')
        self.user = User(username="testUser", email="testUser@test.com", password=self.password)
        
        db.session.add(self.user)
        db.session.commit()

        self.gift = Gift(user_id=self.user.id, title="Test Title", link="link", description="testDescription")
        db.session.add(self.gift)
        db.session.commit()

    def tearDown(self):
        if db.session.query(User).filter_by(id=self.user.id).count() > 0:
            db.session.query(User).filter_by(id=self.user.id).delete()
            db.session.commit()
        if db.session.query(Gift).filter_by(giftid=self.gift.giftid).count() > 0:
            db.session.query(Gift).filter_by(giftid=self.gift.giftid).delete()
            db.session.commit()

    def test_user_existance(self):
        query = db.session.query(User).filter_by(id=self.user.id).one()
        self.assertEqual(query.username, "testUser")

    def test_password(self):
        incorrect_password = secrets.token_hex(len(self.raw_password))
        query = db.session.query(User).filter_by(id=self.user.id).one()
        self.assertEqual(query.password, self.password)
        self.assertTrue(bcrypt.check_password_hash(self.user.password, self.raw_password))
        self.assertFalse(bcrypt.check_password_hash(self.user.password, incorrect_password))

    def test_remove_user(self):
        user_id = self.user.id
        db.session.query(User).filter_by(id=self.user.id).delete()
        count = db.session.query(User).filter_by(id=user_id).count()
        self.assertEqual(count, 0)

    def test_gift_existance(self):
        count = db.session.query(Gift).filter_by(giftid=self.gift.giftid).count()
        self.assertEqual(count, 1)

        query = db.session.query(Gift).filter_by(giftid=self.gift.giftid).one()
        self.assertEqual(self.gift.title, "Test Title")

    def test_add_remove_gift(self):
        giftTwo = Gift(user_id=self.user.id, title="Second Test Title", link="", description="")
        db.session.add(giftTwo)
        db.session.commit()

        count = db.session.query(Gift).filter_by(user_id=self.user.id).count()
        print(db.session.query(Gift).filter_by(user_id=self.user.id).all())
        self.assertEqual(count, 2)

        gift_titles = sorted([gift.title for gift in db.session.query(Gift).filter_by(user_id=self.user.id).all()])
        expected_gift_titles = sorted([giftTwo.title, self.gift.title])
        self.assertEqual(gift_titles, expected_gift_titles)

        db.session.query(Gift).filter_by(giftid=giftTwo.giftid).delete()
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
