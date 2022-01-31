from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Member

class MemberListViewTests(TestCase):
    def test_member(self):
        """
        自分のメンバーがすべて表示される。
        """
        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')
        other = User.objects.create_user('other', password='llamapaca')

        # テストメンバー
        member1 = Member.objects.create(
            owner=user, 
            name='test1', 
            tmgbc_id='11111111', 
            tmgbc_password='11111111',
        )
        member2 = Member.objects.create(
            owner=user, 
            name='test2', 
            tmgbc_id='22222222', 
            tmgbc_password='22222222',
        )
        Member.objects.create(
            owner=other, # other
            name='test3', 
            tmgbc_id='33333333', 
            tmgbc_password='33333333',
        )

        # ログイン
        self.client.force_login(user)

        # メンバーリスト画面をGET
        response = self.client.get(reverse('bulklot:member_list'))

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'メンバー')
        self.assertQuerysetEqual(
            list(response.context['member_list']),
            [member1, member2],
        )


class MemberCreateViewTests(TestCase):
    def test_member(self):
        """
        メンバーを新規登録する。
        """
        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')

        # POSTパラメータ
        name='test1' 
        tmgbc_id='11111111' 
        tmgbc_password='11111111'
        param = {'name': name, 'tmgbc_id': tmgbc_id, 'tmgbc_password': tmgbc_password}

        # ログイン
        self.client.force_login(user)

        # 登録前はメンバーが存在しないこと
        members = Member.objects.filter(name=name)
        self.assertEqual(members.count(), 0)

        # メンバー登録リクエストをPOST
        response = self.client.post(reverse('bulklot:member_create'), param, follow=True)

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'メンバー')
        self.assertContains(response, name)
        members = Member.objects.filter(name=name)
        self.assertEqual(members.count(), 1)

class MemberUpdateViewTests(TestCase):
    def test_member(self):
        """
        メンバーを変更する。
        """
        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')

        # テストメンバー
        name='test1' 
        tmgbc_id='11111111'
        tmgbc_password='11111111'

        member = Member.objects.create(
            owner=user, 
            name=name, 
            tmgbc_id=tmgbc_id, 
            tmgbc_password=tmgbc_password,
        )
        
        # POSTパラメータ
        tmgbc_id_new='22222222'
        param = {'name': name, 'tmgbc_id': tmgbc_id_new, 'tmgbc_password': tmgbc_password}

        # ログイン
        self.client.force_login(user)

        # メンバー変更リクエストをPOST
        response = self.client.post(
            reverse('bulklot:member_update', kwargs={'pk': member.id}),
            param,
            follow=True,
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'メンバー')
        self.assertContains(response, tmgbc_id_new)
        member.refresh_from_db()
        self.assertEqual(member.tmgbc_id, tmgbc_id_new)
        self.assertQuerysetEqual(
            list(response.context['member_list']),
            [member],
        )

class MemberDeleteViewTests(TestCase):
    def test_member(self):
        """
        メンバーを削除する。
        """
        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')

        # テストメンバー
        name='test1' 
        tmgbc_id='11111111'
        tmgbc_password='11111111'

        member = Member.objects.create(
            owner=user, 
            name=name, 
            tmgbc_id=tmgbc_id, 
            tmgbc_password=tmgbc_password,
        )

        # POSTパラメータ
        param = {'name': name, 'tmgbc_id': tmgbc_id, 'tmgbc_password': tmgbc_password}

        # ログイン
        self.client.force_login(user)

        # 削除前はメンバーが存在すること
        members = Member.objects.filter(name=name)
        self.assertEqual(members.count(), 1)

        # メンバー削除リクエストをPOST
        response = self.client.post(
            reverse('bulklot:member_delete', kwargs={'pk': member.id}),
            param,
            follow=True,
        )

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'メンバー')
        self.assertNotContains(response, name)
        members = Member.objects.filter(name=name)
        self.assertEqual(members.count(), 0)



