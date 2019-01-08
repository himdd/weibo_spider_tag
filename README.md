# start
cd src/crawler/  && python scheduler.py

#00 * * * * cd src/downloader/ && python upload_weibo.py >> /tmp/upload.log 2>&1
#00 * * * * cd src/tag/ && python content_to_tag.py >> /tmp/content_to_tag.log 2>&1
