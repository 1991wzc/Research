#!/usr/bin/python
# -*- coding: utf-8 -*-
import MeCab
import sys

m = MeCab.Tagger("-Ochasen")
print m.parse("竹取物語")
