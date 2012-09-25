class EventMixin(object):
    def __unicode__(self):
        return u'%s for %s' % (self.name, self.content_object)
