import unittest
from tool.pdf_link_save import download_pdf
from tool.pdf_link_save import save_to_minio
class pdf_link_save_TestCase(unittest.TestCase):
    def test_pdf_download(self):
        # self.assertEqual(True, False)  # add assertion here
        download_pdf(
            save_path='E:/GitHub/model/google_scholar_spider/test/',
            pdf_name='mytest',
            pdf_url='https://cmpe.boun.edu.tr/~ethem/i2ml/i2ml-figs.pdf'
        )

    def test_minio_download(self):
        # self.assertEqual(True, False)  # add assertion here
        save_to_minio(
            file_path='https://cmpe.boun.edu.tr/~ethem/i2ml/i2ml-figs.pdf',
            file_save_path='/test/mytest.pdf'
        )
if __name__ == '__main__':
    unittest.main()
