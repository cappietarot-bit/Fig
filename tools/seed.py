"""
Build www/data/content.json, the cards the app actually serves.

Every entry names a verse by reference only. The scripture text is looked up out
of www/data/bible.json at build time, so a card can never ship a misquote.

The app cycles each stream independently, so the three streams do not have to be
the same length. Append to CARDS and rerun.

Run:
  "C:\\Users\\levia\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" tools/seed.py
"""

import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIBLE = os.path.join(ROOT, "www", "data", "bible.json")
OUT = os.path.join(ROOT, "www", "data", "content.json")

# stream, reference, quote, gloss, optional story
# A story is (badge, body). "Parable" for ones we write, "Sent in" for real ones,
# and a real one also carries a name and a place.
CARDS = [

    # ---------------------------------------------------------------- receive
    ("receive", "Mark 11:24",
     "Ask once. Then live like the answer already came.",
     "Read the tense. Not that you will receive it. That you received it, said while nothing has moved yet.",
     ("Parable", "She had been turned down for the place twice, so she stopped asking for it. She just started falling asleep in the room instead. She knew where the couch went. She knew which window the morning came through. The call came about a unit that never got listed, and when she walked in she already knew the place.")),

    ("receive", "Matthew 7:7",
     "Knocking is not doubt. It is the sound of someone who expects a door.",
     "Three verbs and three answers, and none of the answers are conditional. The asking is the only variable in the sentence.",
     None),

    ("receive", "Hebrews 11:6",
     "You cannot come to Him hedging.",
     "He is called a rewarder in the same breath as the requirement. Believing that He is, and believing that He pays, are one act.",
     None),

    ("receive", "Matthew 9:29",
     "You are not given what you asked for. You are given what you believed.",
     "According to your faith. Not according to your need, your wording, or how badly you wanted it.",
     ("Parable", "He prayed the same careful sentence every night for a year, and underneath it he assumed nothing would change. Nothing changed. The night he stopped asking and started thanking, the sentence was worse and shorter, and something moved that week. The words were never the thing being answered.")),

    ("receive", "Mark 9:23",
     "The limit was never on His side.",
     "The man asked if He could. He handed the question back. Possible to him that believeth, which puts the word if somewhere else entirely.",
     None),

    ("receive", "Hebrews 11:1",
     "Faith is not the wanting. It is the having, before the proof.",
     "Substance and evidence are both courtroom words. Faith is being entered as the exhibit, not the argument.",
     None),

    ("receive", "Romans 4:17",
     "Speak about it the way He does. As a thing that already is.",
     "He calls things that be not as though they were, and that is not described as poetry. It is described as how the thing gets made.",
     None),

    ("receive", "Isaiah 65:24",
     "The answer left before your question did.",
     "Before they call, I will answer. The delay you are feeling is on the receiving end, not the sending end.",
     None),

    ("receive", "John 16:24",
     "Some things are unasked, not denied.",
     "Hitherto have ye asked nothing. He is not scolding them. He is pointing at an account nobody has drawn on.",
     None),

    ("receive", "Matthew 17:20",
     "It does not take much. It takes real.",
     "A mustard seed is the smallest thing in the illustration. The size was never the problem, and He says so before the mountain moves.",
     None),

    ("receive", "1 John 5:15",
     "Knowing He heard is the same as having it.",
     "The verse does not say we will have. It says we have, and it puts that in the same sentence as knowing He hears.",
     None),

    ("receive", "Matthew 21:22",
     "The believing is the receiving. Nothing comes after it.",
     "All things, whatsoever, believing, ye shall receive. Four words wide open and one condition, and the condition is not effort.",
     None),

    # -------------------------------------------------------------- gratitude
    ("gratitude", "John 11:41",
     "Gratitude is not the receipt. It is the order.",
     "He said it out loud with the stone still in front of the tomb. The thanks came first. The man walked out after.",
     ("Parable", "His brother had not spoken to him in four years. He got tired of asking for it to change, so at night he started thanking God like the call had already come, and picturing the phone lighting up with that name on it. He did it for about two months. The call came on a Sunday afternoon about nothing at all, and neither of them brought up the four years.")),

    ("gratitude", "1 Thessalonians 5:18",
     "In every thing. That is the whole instruction, and it is the hard part.",
     "Not for every thing. In it. The circumstance is where you are standing, not what you are thanking Him for.",
     None),

    ("gratitude", "Psalms 100:4",
     "You do not thank Him once you are inside. The thanks is the gate.",
     "Enter into his gates with thanksgiving. It is written as the means of entry, not as the manners you use after arriving.",
     None),

    ("gratitude", "Psalms 106:1",
     "His mercy is not a mood. It endures.",
     "Endureth for ever is a claim about duration, which means the thing you are afraid you used up cannot be used up.",
     None),

    ("gratitude", "Philippians 4:6",
     "Ask with thanks attached, or you are only worrying out loud.",
     "With thanksgiving let your requests be made known. The thanks is bolted to the request in the same clause, not offered afterward.",
     None),

    ("gratitude", "Psalms 103:2",
     "Forgetting is the only way to be poor.",
     "Forget not all his benefits. The instruction assumes the benefits are already there and that losing track of them is the actual risk.",
     None),

    ("gratitude", "Psalms 34:1",
     "At all times. Especially the ones that have not earned it yet.",
     "At all times, and continually, twice in one verse. He is closing the loophole on purpose.",
     ("Parable", "She started writing down one thing every night, and for the first three weeks it felt like lying. The list was small and ordinary and some nights it was just the heat working. By the spring she noticed she had stopped bracing when the phone rang. Nothing outside had changed yet. She had changed which room she was living in.")),

    ("gratitude", "Psalms 118:24",
     "It was made. Not endured. Made.",
     "This is the day which the LORD hath made. Somebody built it on purpose, which makes rejoicing a reasonable response rather than a forced one.",
     None),

    ("gratitude", "Ephesians 5:20",
     "Always, and for all things, is not a suggestion about tone.",
     "Giving thanks always for all things. Paul writes it as the ordinary condition of a person, not as a reaction to good news.",
     None),

    ("gratitude", "Psalms 50:23",
     "Praise is not the response to the door opening. It is the hinge.",
     "Whoso offereth praise glorifieth me, and the second half of the verse ties it directly to being shown the way out.",
     None),

    ("gratitude", "Colossians 3:15",
     "Be ye thankful is written as a command, which means it is a choice.",
     "It sits right after letting peace rule. The order matters. Thankfulness is what keeps the peace in charge.",
     None),

    ("gratitude", "Psalms 107:1",
     "Say it because it is true, not because you feel it yet.",
     "O give thanks unto the LORD, for he is good. The reason given is His character, not your week.",
     None),

    # ------------------------------------------------------------ restoration
    ("restoration", "Joel 2:25",
     "The years you lost are not gone. They are owed back.",
     "He does not offer to help you make peace with those years. He offers to give them back. Restoration is a return, not a consolation.",
     ("Parable", "He counted the years he had wasted the way a man counts money he no longer has. Someone told him to put the ledger down and write the next page instead, at night, before sleep, and to keep writing it until that page felt more familiar than the old one. It took months. The lost years never came back on a calendar. They came back in what he was finally able to build with what was left.")),

    ("restoration", "Isaiah 43:25",
     "He does not keep the copy that you keep.",
     "Blotteth out, and will not remember. If the record is being wiped on His side, holding your own copy is a decision you are making.",
     None),

    ("restoration", "Psalms 23:3",
     "Restored, not replaced.",
     "He restoreth my soul. It is the same soul, brought back, which is a very different promise from being handed a new one.",
     None),

    ("restoration", "2 Corinthians 5:17",
     "Old things are passed away. Passed. Already.",
     "Every verb in the verse is finished. Become new is not something being scheduled, it is being reported.",
     None),

    ("restoration", "Lamentations 3:23",
     "Mercy does not carry over. It arrives new.",
     "New every morning, written by a man in the middle of a ruined city. He is not describing good circumstances. He is describing supply.",
     None),

    ("restoration", "Isaiah 61:3",
     "Beauty for ashes is a trade, not a comfort.",
     "For is the word doing the work. Something is handed over and something comes back, which means the ashes had to be given up to make the exchange.",
     None),

    ("restoration", "Revelation 21:5",
     "All things. Not the salvageable ones.",
     "Behold, I make all things new. The line is spoken in the present tense about a work already under way.",
     None),

    ("restoration", "Romans 12:2",
     "The mind gets renewed first. Everything else is downstream.",
     "Be ye transformed by the renewing of your mind. The order in the sentence is the order of operations.",
     ("Parable", "Everyone had a reason why the shop would not make it, and most of the reasons were good ones. He stopped arguing with them. At night he sat in the empty room and heard it busy instead, people talking over each other, the door not staying shut. He did that for a year while the numbers said otherwise. The numbers moved second. They always move second.")),

    ("restoration", "Isaiah 1:18",
     "Scarlet is not a stain He is working around.",
     "As white as snow, and the invitation before it is come now, let us reason together. He opens the conversation Himself.",
     None),

    ("restoration", "Psalms 103:12",
     "East and west never meet. That is the point of the measurement.",
     "He could have said north and south, which have poles and therefore a limit. He picked the pair with no meeting point.",
     None),

    ("restoration", "Isaiah 61:4",
     "The ruin is the building material.",
     "They shall build the old wastes and repair the waste cities. Nothing is imported. The wreck itself is what gets raised.",
     None),

    ("restoration", "Isaiah 43:18",
     "You are allowed to stop consulting it.",
     "Remember ye not the former things, neither consider the things of old. Consider is the sharper word. It means stop taking advice from it.",
     None),

    # ============================================================ batch 1
    ("receive", "Ephesians 3:20",
     "You are not asking too much. You are asking too small.",
     "Exceeding abundantly above all that we ask or think. The ceiling named in the verse is your own imagination, and He is described as clearing it.",
     None),

    ("receive", "Psalms 37:4",
     "Delight first. The desires are the second half of the verse for a reason.",
     "The order is not decoration. Delight is the condition and the giving is what follows from it, in that sequence.",
     None),

    ("receive", "Matthew 8:13",
     "He matched the healing to the officer's certainty, not to his rank.",
     "As thou hast believed, so be it done unto thee. The measure taken was the man's conviction, and the servant was well in the same hour.",
     ("Parable", "The officer never went home to check. He asked from the road, heard the answer, and turned around and got on with his day. Everyone remembers what he believed. Almost nobody notices that he stopped supervising it. The two things are the same act.")),

    ("receive", "Mark 10:27",
     "Impossible is a measurement of you, not of it.",
     "He does not argue that the thing is easy. He moves the whole question off the man and onto God, and the word impossible stays where it was.",
     None),

    ("receive", "Luke 11:10",
     "Every one. That is the size of the door.",
     "Every one that asketh receiveth. No qualifier follows it, and He repeats the pattern three times so nobody reads it as a special case.",
     None),

    # ============================================================ batch 2
    ("gratitude", "Psalms 103:1",
     "He is talking to himself. That is allowed.",
     "Bless the LORD, O my soul. David gives his own insides an instruction, which means thanks is something you can order rather than something you wait to feel.",
     None),

    ("gratitude", "Hebrews 13:15",
     "It is called a sacrifice because some days it costs something.",
     "The sacrifice of praise, offered continually. The word admits the price up front and asks for it anyway.",
     ("Parable", "She thanked Him out loud in the car on the worst week of the year and heard how thin her own voice sounded. She did it again the next morning. By the end of the month it had stopped sounding thin, and nothing about the week had improved. Something else had.")),

    ("gratitude", "Habakkuk 3:18",
     "Yet. The whole verse turns on one small word.",
     "Read what sits directly before it. No fruit on the vine, no herd in the stall, nothing in the field. Then yet I will rejoice.",
     None),

    ("gratitude", "1 Corinthians 15:57",
     "He wrote the victory in the present tense. Use the tense He used.",
     "Giveth us the victory. Not will give. Paul reports it as ongoing supply rather than a date on a calendar.",
     None),

    ("gratitude", "Psalms 92:1",
     "It is good for you before it is anything else.",
     "It is a good thing to give thanks. Named as beneficial, not as owed, which puts thanks closer to food than to manners.",
     None),

    # ============================================================ batch 3
    ("restoration", "Psalms 51:10",
     "Create. He asked for new, not repaired.",
     "Create is the word Genesis uses for making something out of nothing. David does not ask for the old heart cleaned up, and he asks this at his lowest point.",
     None),

    ("restoration", "Romans 8:1",
     "Now. Not once you have finished fixing it.",
     "There is therefore now no condemnation. Paul sets the timing in the middle of the sentence where it cannot be quietly moved to later.",
     None),

    ("restoration", "Micah 7:19",
     "The depths. Not the shallows, where you could wade back out and find them.",
     "Cast all their sins into the depths of the sea. In the ancient world that named the one place nothing was ever recovered from.",
     None),

    ("restoration", "Isaiah 40:31",
     "Waiting is not the pause before the strength. It is where it is made.",
     "They that wait upon the LORD shall renew their strength. The waiting is the verb that produces the renewal, not the delay in front of it.",
     ("Parable", "Nothing happened for eleven months and he called that failure. Looking back later he could not point at the week things turned, because there was not one. There was a long flat stretch where he kept showing up, and then a season where he had the strength for what arrived. The flat stretch was not the wait for it. It was it.")),

    ("restoration", "Psalms 103:5",
     "Renewed, not merely remembered.",
     "Satisfieth thy mouth with good things, so that thy youth is renewed. The renewal follows the filling, which puts supply first and recovery second.",
     None),

    # ============================================================ batch 4
    ("receive", "John 15:7",
     "Abiding is the condition. After that the asking is left wide open.",
     "Ask what ye will. The blank is deliberately blank, and the only thing filled in ahead of it is where you have been living.",
     None),

    ("receive", "Luke 1:37",
     "Nothing. It is a short verse because it does not need qualifying.",
     "Six words with no exception clause, and they are spoken to a woman who has just been told something biologically absurd.",
     None),

    ("receive", "James 1:6",
     "A wave does not get anywhere, and it moves all day.",
     "Driven with the wind and tossed. The picture is not of stillness failing. It is of constant motion that never arrives, which is what doubt actually looks like.",
     None),

    ("receive", "Mark 5:34",
     "He credited her, not Himself. Notice that.",
     "Thy faith hath made thee whole. He had the power and still named hers as the thing that did it, and He said it in front of a crowd.",
     None),

    ("receive", "Matthew 6:8",
     "You are not informing Him. You are agreeing with Him.",
     "Your Father knoweth what things ye have need of, before ye ask him. If the need is already known, the asking is not for His benefit.",
     ("Parable", "He used to explain the situation to God in detail, the way you brief someone who just walked in. One night he ran out of preamble and only said the last line, the part he actually wanted. It felt rude. It was the first time he had asked instead of argued.")),

    # ============================================================ batch 5
    ("gratitude", "Psalms 118:1",
     "The reason given is His character, not your week.",
     "For he is good. The verse hands you the grounds up front, so you are not required to find them somewhere in your circumstances.",
     None),

    ("gratitude", "Colossians 1:12",
     "You were made fit for it. That already happened.",
     "Hath made us meet to be partakers. Past tense, and done to you, which means qualifying for the inheritance is not this year's project.",
     None),

    ("gratitude", "Jonah 2:9",
     "He said it from inside the fish, before anything opened.",
     "The thanksgiving is offered in chapter two. He is not put back on dry land until the verse after it.",
     ("Parable", "The letter had not come and he thanked God for it anyway, which felt like lying and he said so out loud. He kept doing it because he could not think of anything better to do. When it finally came he noticed he was not surprised, and that turned out to be the whole point.")),

    ("gratitude", "Psalms 30:12",
     "Silence is the thing being ruled out.",
     "And not be silent. The verse treats saying nothing as the failure state rather than as neutral ground.",
     None),

    ("gratitude", "Psalms 147:7",
     "Sung, not thought. Out loud is part of the instruction.",
     "Sing unto the LORD with thanksgiving. Every verb in the verse is audible, which makes gratitude an act rather than a mood.",
     None),

    # ============================================================ batch 6
    ("restoration", "Ezekiel 36:26",
     "The stone is taken out. It is not softened.",
     "Take away, and give. Two separate actions in one verse, which means the hardness gets removed rather than worked on.",
     None),

    ("restoration", "Jeremiah 30:17",
     "He heard what they called you, and answered that.",
     "Because they called thee an Outcast. The reason given for the healing is the name other people put on you, which He quotes back before undoing it.",
     None),

    ("restoration", "1 John 1:9",
     "Faithful and just. Not merely willing.",
     "Both are legal words. The verse frames the cleansing as something owed and reliable rather than something begged for and hoped over.",
     None),

    ("restoration", "Isaiah 58:12",
     "The ruin becomes your title.",
     "Thou shalt be called The repairer of the breach. The thing that broke is renamed as the work you are known for.",
     ("Parable", "For years the worst thing that happened to her was the thing she never mentioned. Then a younger woman asked her about it directly and she answered, and watched the younger woman's shoulders come down. She has been asked about it many times since. It is the only part of her life anyone needs.")),

    ("restoration", "Psalms 126:4",
     "Dry riverbeds. They fill in a single night when the rain comes.",
     "As the streams in the south. Those beds sit empty most of the year, and the image was chosen for how fast they run once they fill.",
     None),

    # ============================================================ batch 7
    ("receive", "Matthew 15:28",
     "Even as thou wilt. He let her set the terms.",
     "She had been turned away twice and kept going anyway. The wording of the answer hands the outcome back to her own will.",
     ("Parable", "She was told no by two different people whose job it was to say no. She did not get angry and she did not leave. She asked again the next week, and the week after, in the same even voice. The third person said yes and acted like it had never been a question.")),

    ("receive", "Hebrews 4:16",
     "Boldly. That one word is doing all the work.",
     "Come boldly unto the throne of grace. The posture named is confidence rather than apology, and it is written as an instruction.",
     None),

    ("receive", "Psalms 34:10",
     "Shall not want any good thing. Read that again, slowly.",
     "The young lions do lack and suffer hunger, and the verse sets them directly against those who seek Him. The comparison is deliberate.",
     None),

    ("receive", "Mark 10:52",
     "He was told to be quiet, and he got louder.",
     "The crowd rebuked Bartimaeus and he cried out the more a great deal. The persistence sits in the verses just before the healing.",
     None),

    ("receive", "1 John 3:22",
     "Whatsoever. He keeps returning to that word.",
     "And whatsoever we ask, we receive of him. John writes it as a settled habit rather than an occasional event.",
     None),

    # ============================================================ batch 8
    ("receive", "John 14:13",
     "In my name means in His nature, not as a password.",
     "That will I do, that the Father may be glorified. The purpose clause tells you what kind of asking fits inside the name.",
     None),

    ("receive", "James 4:3",
     "Sometimes the no is about the wanting, not the asking.",
     "Ye ask amiss. The verse names a way of asking that fails, which quietly means there is a way that does not.",
     None),

    ("receive", "Luke 18:42",
     "Receive. It is an instruction, not a parcel being handed over.",
     "Receive thy sight is phrased as a command to the man, which puts an action back on his side of the exchange.",
     None),

    ("gratitude", "1 Chronicles 16:8",
     "Tell somebody. That is part of the instruction.",
     "Make known his deeds among the people. Gratitude here is not private. It ends with someone else hearing about it.",
     None),

    ("gratitude", "Psalms 116:17",
     "Thanks first, then the asking. In that order.",
     "The sacrifice of thanksgiving is in the first half of the verse and the calling on His name is in the second.",
     None),

    # ============================================================ batch 9
    ("gratitude", "Daniel 2:23",
     "He thanked Him for the answer before he told anyone he had it.",
     "Daniel praises in private on the night the secret is revealed, and only afterwards goes to the king with it.",
     ("Parable", "The number came back the way he had hoped and his first instinct was to call everybody. He sat in the car instead and said thank you out loud to nobody visible, for about a minute. He says that minute is the only part of that day he can still feel.")),

    ("gratitude", "Luke 17:16",
     "Ten were healed. One came back.",
     "All ten were cleansed on the road. The one who turned around is the only one who hears thy faith hath made thee whole.",
     None),

    ("gratitude", "Psalms 9:1",
     "Whole heart. Not the part that is currently satisfied.",
     "I will praise thee with my whole heart. The measure named is the whole of him, which rules out praising with the convenient half.",
     None),

    ("gratitude", "Psalms 63:3",
     "Better than life. He weighed the two and said so.",
     "Because thy lovingkindness is better than life. The praise in the second half follows from that valuation rather than from circumstances.",
     None),

    ("gratitude", "Psalms 95:2",
     "It is how you arrive, not what you say once you are inside.",
     "Let us come before his presence with thanksgiving. Same idea as the gates in Psalm 100. Thanks is the approach itself.",
     None),

    # ============================================================ batch 10
    ("gratitude", "Colossians 3:17",
     "Whatsoever ye do. It is meant to sit underneath everything.",
     "In word or deed, giving thanks. Paul does not carve out a category of ordinary tasks that are exempt from it.",
     None),

    ("restoration", "Romans 4:18",
     "Against hope, he believed in hope. Both at once.",
     "Who against hope believed in hope. The facts were not on his side and he was not pretending they were. He refused to build on them.",
     None),

    ("restoration", "Isaiah 43:19",
     "Now it shall spring forth. Not eventually.",
     "I will do a new thing, now it shall spring forth, shall ye not know it. He asks whether you will recognise it, which assumes it is already starting.",
     ("Parable", "The change was so small the first month that she kept checking whether anything was happening at all. Looking back she can name the week it started, and at the time it looked like nothing. It looked like her getting up slightly earlier and not explaining why.")),

    ("restoration", "Psalms 103:3",
     "All, and all. He used the word twice in one verse.",
     "Who forgiveth all thine iniquities, who healeth all thy diseases. Two clauses, the same total word in each, and no exception listed in either.",
     None),

    ("restoration", "Zechariah 9:12",
     "Prisoners of hope. He is the one who named you that.",
     "Turn you to the strong hold, ye prisoners of hope. The same verse promises to render double, so the holding is temporary by design.",
     None),

    # ============================================================ batch 11
    ("restoration", "Psalms 85:6",
     "Again. It has happened before, which is why he can ask.",
     "Wilt thou not revive us again. The request leans on a precedent, and the reviving is tied to the people rejoicing rather than to their deserving.",
     None),

    ("restoration", "Isaiah 54:4",
     "You will forget it. That is listed as part of the repair.",
     "Thou shalt forget the shame of thy youth. Forgetting is named as an outcome He provides, not as something you have to manufacture.",
     None),

    ("restoration", "Joel 2:26",
     "Plenty and satisfied are two different promises.",
     "Ye shall eat in plenty, and be satisfied. A person can have plenty and stay hungry, so the verse says both on purpose.",
     None),

    ("restoration", "Psalms 107:20",
     "He sent a word. That was the whole intervention.",
     "He sent his word, and healed them, and delivered them. Nothing else is described as being done, and both results follow from the sending.",
     None),
]

REF = re.compile(r"^(.+?)\s+(\d+):(\d+)(?:\s*[-\u2013]\s*(\d+))?$")


def load_bible():
    with io.open(BIBLE, encoding="utf-8") as fh:
        data = json.load(fh)
    return {b["n"]: b["c"] for b in data["books"]}


def lookup(bible, ref):
    m = REF.match(ref.strip())
    if not m:
        raise SystemExit("cannot parse reference: %r" % ref)
    book, chap, first, last = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    if book not in bible:
        raise SystemExit("no such book: %r (in %r)" % (book, ref))
    chapters = bible[book]
    if chap < 1 or chap > len(chapters):
        raise SystemExit("%s has no chapter %d" % (book, chap))
    verses = chapters[chap - 1]
    last = int(last) if last else first
    if first < 1 or last > len(verses):
        raise SystemExit("%s %d has no verse %d" % (book, chap, last))
    text = " ".join(verses[first - 1:last])
    return book, chap, first, last, text


def main():
    bible = load_bible()
    streams = {}

    for stream, ref, quote, gloss, story in CARDS:
        book, chap, first, last, text = lookup(bible, ref)
        card = {
            "ref": ref,
            "book": book, "chapter": chap, "verse": first, "verseEnd": last,
            "text": text,
            "quote": quote,
            "gloss": gloss,
        }
        if story:
            card["story"] = {"badge": story[0], "body": story[1]}
        streams.setdefault(stream, []).append(card)

    out = {
        "translation": "King James Version",
        "license": "public domain",
        "streams": streams,
    }
    with io.open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    shortest = min(len(v) for v in streams.values())
    for name in ("receive", "gratitude", "restoration"):
        cards = streams.get(name, [])
        stories = sum(1 for c in cards if "story" in c)
        print("%-12s %2d cards, %d with a story" % (name, len(cards), stories))
    print("\n%d days before anything repeats -> %s" % (shortest, OUT))


if __name__ == "__main__":
    main()
