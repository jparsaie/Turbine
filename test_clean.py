__author__ = 'jparsaie'

import unittest
import os
import shutil
import d_clean

distroDirectory = "testDistro"

class TestStringMethods(unittest.TestCase):

    #Called before the beginning of every test.
    @classmethod
    def setUpClass(cls):
        cls.cwd = "E:\/"

        #Remove old main distro directory and create a new one.
        shutil.rmtree(os.path.join(cls.cwd, distroDirectory), ignore_errors=True)
        os.mkdir(os.path.join(cls.cwd, distroDirectory))

    #Called at the end of entire test run.
    @classmethod
    def tearDown(cls):
        #Remove main distro directory after suite run complete.
        shutil.rmtree(os.path.join("E:\/", distroDirectory), ignore_errors=True)

    #Provided a version directory and list of distros, return a Boolean
    #value specifying if given version exists in list.
    def version_in_distro_list(self, version, distro_list):
        for d in distro_list:
            if version in d.encode('string-escape'):
                return True
        return False

    def test_minimal(self):
        #Set up service(s), revision(s), and distro(s)
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.0"))

        #Get list of all distros, and list of distros kept/discarded
        distros = d_clean.get_distro_list(os.path.join(self.cwd, distroDirectory, "service"))
        keep, discard = d_clean.get_keep_discard_list(distros, os.path.join(self.cwd, distroDirectory, "service"))

        #Verify that one distro is kept (1.0), and none were discarded
        self.assertEqual(1, len(keep))
        self.assertIn('1.0', distros[0])
        self.assertEqual(0, len(discard))

    def test_basic_one_major_revision(self):
        #Set up service(s), revision(s), and distro(s)
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.0"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.2"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.4"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.6"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.8"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.13"))

        #Get list of all distros, and list of distros kept/discarded
        distros = d_clean.get_distro_list(os.path.join(self.cwd, distroDirectory, "service"))
        keep, discard = d_clean.get_keep_discard_list(distros, os.path.join(self.cwd, distroDirectory, "service"))

        #Verify that 5 distros kept, and 1 discarded.
        #Verify that correct distros are in their respected lists.
        self.assertEqual(5, len(keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.13', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.8', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.6', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.4', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.2', keep))
        self.assertEqual(1, len(discard))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.0', discard))

    def test_basic_multiple_major_revision(self):
        #Set up service(s), revision(s), and distro(s)
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.0"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.4"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.0", "1.5"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.1", "1.2"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.1", "1.3"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service", "1.1", "1.4"))


        #Get list of all distros, and list of distros kept/discarded
        distros = d_clean.get_distro_list(os.path.join(self.cwd, distroDirectory, "service"))
        keep, discard = d_clean.get_keep_discard_list(distros, os.path.join(self.cwd, distroDirectory, "service"))

        #Verify that 5 distros kept, and 1 discarded.
        #Verify that correct distros are in their respected lists.
        self.assertEqual(5, len(keep))
        self.assertTrue(self.version_in_distro_list(r'1.1\\1.4', keep))
        self.assertTrue(self.version_in_distro_list(r'1.1\\1.3', keep))
        self.assertTrue(self.version_in_distro_list(r'1.1\\1.2', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.5', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.4', keep))
        self.assertEqual(1, len(discard))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.0', discard))

    def test_basic_multiple_services(self):
        #Set up service(s), revision(s), and distro(s)
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service1", "1.0", "1.0"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service1", "1.0", "1.2"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service1", "1.0", "1.4"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service1", "1.0", "1.6"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service1", "1.0", "1.8"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service1", "1.0", "1.12"))

        os.makedirs(os.path.join(self.cwd, distroDirectory, "service2", "1.0", "1.0"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service2", "1.0", "1.11"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service2", "1.0", "1.12"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service2", "1.0", "1.24"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service2", "1.0", "1.32"))
        os.makedirs(os.path.join(self.cwd, distroDirectory, "service2", "1.0", "1.48"))


        #Get list of all distros, and list of distros kept/discarded
        distros = d_clean.get_distro_list(os.path.join(self.cwd, distroDirectory, "service1"))
        keep, discard = d_clean.get_keep_discard_list(distros, os.path.join(self.cwd, distroDirectory, "service1"))

        #Verify that 5 distros kept, and 1 discarded for service1.
        #Verify that correct distros are in their respected lists for service1.
        self.assertEqual(5, len(keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.12', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.8', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.6', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.4', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.2', keep))
        self.assertEqual(1, len(discard))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.0', discard))

        #Get list of all distros, and list of distros kept/discarded
        distros = d_clean.get_distro_list(os.path.join(self.cwd, distroDirectory, "service2"))
        keep, discard = d_clean.get_keep_discard_list(distros, os.path.join(self.cwd, distroDirectory, "service2"))

        #Verify that 5 distros kept, and 1 discarded for service2.
        #Verify that correct distros are in their respected lists for service2.
        self.assertEqual(5, len(keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.11', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.12', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.24', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.32', keep))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.48', keep))
        self.assertEqual(1, len(discard))
        self.assertTrue(self.version_in_distro_list(r'1.0\\1.0', discard))

    def test_no_minor(self):
        #Set up service(s), revision(s), and distro(s)
        os.makedirs(os.path.join(self.cwd, "testDistro", "service"))
        os.makedirs(os.path.join(self.cwd, "testDistro", "service", "1.0"))

        #Get list of all distros, and list of distros kept/discarded
        distros = d_clean.get_distro_list(os.path.join(self.cwd, distroDirectory, "service"))
        keep, discard = d_clean.get_keep_discard_list(distros, os.path.join(self.cwd, distroDirectory, "service"))

        #Verify that keep and discard are empty. No results.
        self.assertEqual(0, len(keep))
        self.assertEqual(0, len(discard))

if __name__ == '__main__':
    unittest.main()