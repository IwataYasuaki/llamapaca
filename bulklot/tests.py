from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Member, LotResult
from datetime import date

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

class LotReqCreateViewTests(TestCase):
    def test_member(self):
        """
        自分のメンバーのみ選べること。
        """
        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')
        other = User.objects.create_user('other', password='llamapaca')

        # テストメンバー
        my_member = Member.objects.create(
            owner=user, 
            name='my_member', 
            tmgbc_id='11111111', 
            tmgbc_password='11111111',
        )
        others_member = Member.objects.create(
            owner=other, 
            name='others_member', 
            tmgbc_id='22222222', 
            tmgbc_password='22222222',
        )

        # ログイン
        self.client.force_login(user)

        # 抽選申込フォームをGET
        response = self.client.get(reverse('bulklot:lot_req_create'))

        # assert
        members = response.context['lotreqtime_formset'][0].fields['member'].queryset
        self.assertQuerysetEqual(members, [my_member])

class LotReqDetailViewTests(TestCase):
    def test_member(self):
        """
        自分のメンバーのみ選べること。
        """
        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')
        other = User.objects.create_user('other', password='llamapaca')

        # テストメンバー
        my_member = Member.objects.create(
            owner=user, 
            name='my_member', 
            tmgbc_id='11111111', 
            tmgbc_password='11111111',
        )
        others_member = Member.objects.create(
            owner=other, 
            name='others_member', 
            tmgbc_id='22222222', 
            tmgbc_password='22222222',
        )

        # ログイン
        self.client.force_login(user)

        # 抽選申込フォームをGET
        response = self.client.get(reverse('bulklot:lot_req_create'))

        # assert
        members = response.context['lotreqtime_formset'][0].fields['member'].queryset
        self.assertQuerysetEqual(members, [my_member])

class LotResultListViewTests(TestCase):
    def test_result(self):
        """
        自分の抽選結果が表示される。
        """
        today = date.today()

        # テストユーザ
        user = User.objects.create_user('tester', password='llamapaca')
        other = User.objects.create_user('other', password='llamapaca')

        # テストメンバー
        my_member = Member.objects.create(
            owner=user, 
            name='my_member', 
            tmgbc_id='11111111', 
            tmgbc_password='11111111',
        )
        others_member = Member.objects.create(
            owner=other, 
            name='others_member', 
            tmgbc_id='22222222', 
            tmgbc_password='22222222',
        )

        # テスト抽選結果
        my_active_result = LotResult.objects.create(
            owner=user,
            member=my_member,
            datetime='2022年6月25日 土曜日 15時～17時',
            sport='テニス（人工芝）',
            location='舎人公園',
            result='○',
            pubdate=today,
            active=True,
        )
        my_inactive_result = LotResult.objects.create(
            owner=user,
            member=my_member,
            datetime='2022年6月25日 土曜日 15時～17時',
            sport='テニス（人工芝）',
            location='舎人公園',
            result='○',
            pubdate=today,
            active=False,
        )
        others_active_result = LotResult.objects.create(
            owner=other,
            member=others_member,
            datetime='2022年6月25日 土曜日 15時～17時',
            sport='テニス（人工芝）',
            location='舎人公園',
            result='○',
            pubdate=today,
            active=True,
        )

        # ログイン
        self.client.force_login(user)

        # メンバーリスト画面をGET
        response = self.client.get(reverse('bulklot:lot_result_list'))

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '抽選結果')
        self.assertQuerysetEqual(
            list(response.context['lotresult_list']),
            [my_active_result,],
        )

