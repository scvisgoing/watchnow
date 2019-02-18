"""
Test views
"""
#from django.test import TestCase
from django.urls import reverse # from django.core.urlresolvers import reverse
#from rest_framework.test import APIClient
from rest_framework.test import APITestCase # 這個預設用的就是 APIClient 而不是 dj 的 Client
from rest_framework import status

from monitor.models import Host

#class HostViewTestCase(TestCase):
class HostViewTestCase(APITestCase):
    """Test suite for the api views CRUD"""

    def setUp(self):
        """Define the test client and other test variables."""
        #self.client = APIClient()
        self.host_data = {'name': 'VimTest-DEV', 'ipv4':'10.62.41.100'}
        self.response = self.client.post(reverse('host-list'), self.host_data, format="json")

    def test_create_a_host(self):
        """Test the api has host creation capability."""
        print('@@@ response.data:', self.response.data)
        print('@@@ response.json():', self.response.json())
        # settings 中若有定義 DEFAULT_PERMISSION_CLASSES 則會導致 403 錯誤
        # {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_a_host(self):
        """Test the api can get a given host."""
        host = Host.objects.get()
        response = self.client.get(reverse('host-detail', kwargs={'pk': host.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, host)

    def test_get_many_hosts(self):
        """Test the api can get host list."""
        host_data = {'name': 'VimTest-DEV01', 'ipv4':'10.62.41.101'}
        response = self.client.post(reverse('host-list'), host_data, format="json")
        host_data = {'name': 'VimTest-DEV02', 'ipv4':'10.62.41.102'}
        response = self.client.post(reverse('host-list'), host_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # 先確認產生兩筆 ok

        response = self.client.get(reverse('host-list'), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Host.objects.count(), 3)                       # 確認拿到的 list 有三筆

    def test_update_host(self):
        """Test the api can update a given host."""
        host = Host.objects.get() # 目前只有一台 host
        change_name = {'name': 'Wow-DEV'} # 若用 put change_name就得全塞
        res = self.client.patch(reverse('host-detail', kwargs={'pk': host.id}),
                                change_name, format='json')
        #print('有疑問的時後 response.json():', res.json())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # 改完 db 後要再取一次，變數的資料才會正確
        host = Host.objects.get()
        self.assertEqual(host.name, 'Wow-DEV')

    def test_delete_host(self):
        """Test the api can delete a host."""
        host = Host.objects.get()
        res = self.client.delete(reverse('host-detail', kwargs={'pk': host.id}),
                                 format='json', follow=True)
        # 成功的話 res.data = None

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Host.objects.count(), 0)
