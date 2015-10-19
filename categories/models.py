# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.utils.translation import ugettext_lazy  as _
from django.db import models
from django.forms import ModelForm
from documents.models import Document
from django.conf import settings
import os

class TypeCategory(models.Model):
    name = models.CharField(_("Type of documents"), max_length=128)
    priority = models.IntegerField(_('Priority'), unique=True)
    active = models.BooleanField(_('active'), default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    cat = models.ForeignKey(TypeCategory)
    documents = models.ManyToManyField(Document, verbose_name=_('documents'), blank=True)
    refer_trimester = models.ForeignKey('trimesters.Trimester', verbose_name=_('trimester'), related_name="back_trimester", null=True)
    active = models.BooleanField(_('active'), default=True)

    def get_name(self):
        return u'%s' % (self.cat.name)

    def __str__(self):
        return u'%s - %s' % (self.refer_trimester, self.get_name())

    def add_doc(self, document):
        self.documents.add(document)

    def get_docs(self):
        return sorted(self.documents.all(), key=lambda x: x.date, reverse=True)

    def count_docs(self):
        return len(self.documents.all())

    def get_doc(self,i):
        if i < self.count_docs():
            return self.documents.all().order_by('pk')[i]

    def as_json(self):
        return dict(id=self.id, name=self.cat.name, n=str(self.count_docs()), ) 

    def get_relative_path(self):
        return os.path.join(self.refer_trimester.get_relative_path(), self.cat.name)

    def get_absolute_path(self):
        return os.path.join(self.refer_trimester.get_absolute_path(), self.cat.name)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        os.mkdir( self.get_absolute_path(), 0711 );

    def delete(self):
        for d in self.documents.all():
            d.delete()
        os.rmdir(self.get_absolute_path())
        super(Category, self).delete()
    