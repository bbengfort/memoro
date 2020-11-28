# Memorandi

**A simple thought recording tool for personal use.**

[![The Inner Chapters][butterfly_dream.jpg]][butterfly_dream.jpg]

This simple project is intended to be a personal recording tool to capture private snippets from my own inner chapters. It is purposefully simple - there is only one user, me. A responsive front-end allows me to write from anywhere or any device. The main interface is data entry with a secondary catalog for me to review historical thoughts. Other APIs provide access to weather, photos, calendar etc. to link my day with their events.

## Structure

This project isn't intended to be theraputic, but rather obeservational. It was inpsired from two sources: _The Inner Chapters_ by Zhuangzi as well as read snippets from Arthur C. Clarke's journal. What is to be recorded is past tense observations of my work and my daily life as well as the meta data that I experienced but do not put into narrative form (weather, location, etc). A good guide is [Introduction to Journal-Style Scientific Writing][htw_general].

Data Elements included for a daily entry:

1. Location (using GeoIP or some other technique)
2. Weather (fetched via an API based on location)
3. The time and date (obviously)
4. Some narrative of the events of the day (500 words or so)
5. Descriptive tags or labels (more thought required)

<!-- References -->
[butterfly_dream.jpg]: http://www.rescen.net/Chris_Bannerman/images/Illus_01_full.jpg
[htw_general]: http://abacus.bates.edu/~ganderso/biology/resources/writing/HTWgeneral.html
