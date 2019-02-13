from django.test import TestCase

from monitor.models import Host

class TestMovieHost(TestCase):
    def setUp(self):
        func_name = self.shortDescription()    

    def test_host_creation(self):
        host = Host(name='VimDesktop-DEV', ipv4='10.62.41.51')
        host.save()
        self.assertEqual(Host.objects.count(), 1)
        self.assertEqual(host.name, str(host))
        self.assertEqual(host.ipv4, '10.62.41.51')
        self.assertEqual(host.bound_for, None)

    def build_bound_for(self):
        self.bound_host = Host(name='VimDesktop-BBB', ipv4='10.62.40.88')
        self.bound_host.save()
        self.host = Host(name='VimDesktop-DEV', ipv4='10.62.41.51', bound_for=self.bound_host)
        self.host.save()
        self.assertEqual(Host.objects.count(), 2)
        self.assertEqual(self.host.ipv4, '10.62.41.51')
        self.assertEqual(self.bound_host.ipv4, '10.62.40.88')
        self.assertEqual(self.host.bound_for, self.bound_host)
        self.assertEqual(self.bound_host.bebound.get(), self.host)
        #print('@@@@@', self.bound_host.bebound.get())

    #def test_bound_for(self):
    #    self.build_bound_for()
    def test_bound_for_delete_host(self):
        self.build_bound_for()
        print(f'I like host {self.host} bound {self.bound_host}')
        self.host.delete() # 只刪除db 這instance仍有資料
        self.assertEqual(Host.objects.count(), 1)
        self.assertNotEqual(self.host, None)
        self.assertEqual(self.bound_host.ipv4, '10.62.40.88')

    def test_bound_for_delete_bound_host(self):
        self.build_bound_for()
        self.bound_host.delete() # 只刪除db，此時 self.host(有相依它)要重載一次才會正確反應
        self.assertEqual(Host.objects.count(), 1)
        print(f'I check 111 host bound {self.host.bound_for}')
        self.host = Host.objects.get(name='VimDesktop-DEV')
        print(f'I check 222 host bound {self.host.bound_for}')

     
        