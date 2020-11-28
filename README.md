# Memoro

**A simple thought recording tool for personal use.**

[![The Inner Chapters][butterfly_dream.jpg]][butterfly_dream.jpg]

This simple project is intended to be a personal recording tool to capture private snippets from my own inner chapters. It is purposefully simple - there is only one user, me. A responsive front-end allows me to write from anywhere or any device. The main interface is data entry with a secondary catalog for me to review historical thoughts. Other APIs provide access to weather, photos, calendar etc. to link my day with their events.

## Structure

This project isn't intended to be theraputic, but rather obeservational. It was inpsired from three sources: _The Inner Chapters_ by Zhuangzi, snippets from Arthur C. Clarke's journal, and _The Truth of Fact, The Truth of Feeling_ by Ted Chiang. What is to be recorded is past tense observations of my work and my daily life as well as the meta data that I experienced but do not put into narrative form (weather, location, etc). A good guide is [Introduction to Journal-Style Scientific Writing][htw_general]. The point is to capture the

Data Elements included for a daily entry:

1. Location (using GeoIP or some other technique)
2. Weather (fetched via an API based on location)
3. The time and date (obviously)
4. Some narrative of the events of the day (500 words or so)
5. Descriptive tags or labels (more thought required)


Other elements that might be fetched:

1. Top headlines for the day
2. Photos of the day from Google Photos or another source
3. Tweets that I tweeted that day
4. Books I'm currently reading (from Goodreads)
5. Daily health data from Apple Watch
5. Number of tabs that I have open
6. Articles I read that day that were meaningful


The point of any element on the page is to give context into my thought processes for the day.

<!-- References -->
[butterfly_dream.jpg]: http://www.rescen.net/Chris_Bannerman/images/Illus_01_full.jpg
[htw_general]: http://abacus.bates.edu/~ganderso/biology/resources/writing/HTWgeneral.html

## Other Notes

[Definition _memorandi_](https://www.wordsense.eu/memorandi/): Future passive participle of memorō‎; "which is to be reminded".

> Jijingi tells Moseby that the word “true” has two words in their language. "Vough" is factual truth while "mimi" is that which is best for the involved people. The truth of fact and the truth of feeling are weighed equally. This difference plays a central role later on when a dispute threatens to split the tribes apart.
>
> &mdash; [Ted Chiang](https://formalsystem.wordpress.com/tag/chiang/)

