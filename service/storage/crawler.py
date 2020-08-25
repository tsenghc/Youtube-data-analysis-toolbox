from service.storage.models import Subscriptions

if __name__ == '__main__':
    tt = Subscriptions(resourceChannelId="13211233", originalChannelId="3213", subscriptAt="12311231",
                       resourceTitle="as32d", resourceDescription="dads54")
    tt.save_to_db()
