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

# Parables for cards that were written without one, keyed by reference. Kept
# apart from CARDS so stories can be filled in a batch at a time without
# touching a line of the card that is already right. All of these are Parables,
# so none of them carries a name. A real testimony goes in CARDS with the
# "Sent in" badge and a first name and city.
# Full length stories: 3 paragraphs of 5 to 7 sentences, plus 2 or 3
# parables that light up different moments in the story. The app reveals them in
# stages, one paragraph, then the rest, then the parables.
#
# As a card is written to full length it moves out of EXTRA_STORIES below and
# into here. Both shapes work at once, so the app is never broken half way
# through the rewrite, and seed.py reports how many are still short.
FULL = {

    "Mark 11:24": {
        "paragraphs": [
            {
                "text": "She had been turned down for the apartment twice, and the second refusal came by voicemail while she was standing in the queue at the bank. The woman on the message was kind about it, which somehow made it worse. She had done everything right both times. She had the deposit, the references, the letter from her manager, and none of it counted for anything against forty other people who had those too. She deleted the message in the car and sat there a while without turning the key.",
                "links": [{
                    "phrase": "turned down for the apartment twice",
                    "ref": "Matthew 15:23",
                    "moment": "A woman asks him for her daughter and he answers her not a word. His own disciples ask him to send her away. She is refused twice before anything turns, and she does not leave.",
                }],
            },
            {
                "text": "What she stopped doing that month was asking. Not out of bitterness, and not because she had let the place go, but because she had heard something in the way she asked. Underneath the words there was a small grinding sound, like somebody pushing a door that opens the other way. She could hear that she did not expect anything. So she stopped, and instead she started going to sleep in the apartment, which is the only way she knows how to say it. She would lie down in her mother's spare room and put herself in the other place and stay there until it was ordinary, until she was bored in it, putting a mug down, looking for a charger.",
                "links": [
                    {
                        "phrase": "she did not expect anything",
                        "ref": "James 1:6",
                        "moment": "The one who wavers is a wave driven with the wind and tossed. Not still, not lazy, just in motion all day without arriving anywhere.",
                    },
                    {
                        "phrase": "going to sleep in the apartment",
                        "ref": "Genesis 28:11",
                        "moment": "Jacob lies down for the night in a place he is only passing through, with a stone for a pillow, and is told in his sleep that the ground he is lying on is already given to him.",
                    },
                ],
            },
            {
                "text": "Six weeks went by with nothing at all, and she kept doing it, mostly because stopping would have been a decision she did not want to make. Then the manager called about a unit that had never been listed, one floor up in the same building. She heard herself accept it in a voice that surprised her, because it was not the voice of someone getting good news. It was the voice of someone confirming an arrangement. The strangest part was walking in, because there was no rush of relief, and for a day or two she wondered what was wrong with her. What she was missing is the feeling of getting something you did not have. All that was left was to bring the boxes.",
                "links": [
                    {
                        "phrase": "Six weeks went by with nothing at all",
                        "ref": "1 Kings 18:43",
                        "moment": "Elijah sends his servant to look toward the sea and the servant comes back with nothing, seven times over. Elijah had already told the king to go and eat, because he could hear rain that had not started.",
                    },
                    {
                        "phrase": "the voice of someone confirming an arrangement",
                        "ref": "Hebrews 11:1",
                        "moment": "Substance and evidence are both words from a courtroom. Faith is entered as the exhibit rather than argued as the case.",
                    },
                ],
            },
        ],
    },
}


EXTRA_STORIES = {

    # ---------------------------------------------------------- receive
    "Matthew 7:7":
    "She sent the same application to the same company four times over two years. Friends told her it was starting to look desperate. She could not explain that from the inside it did not feel desperate, it felt like arriving early. The fourth time, a new manager read it and asked why she had not applied sooner. She had. Nobody had opened the door yet.",

    "Hebrews 11:6":
    "He prayed for the business and kept a second plan running quietly underneath it, the way you keep a hand on a door. Both plans got half of him and neither one moved. The month he shut the second plan down was not the month he felt brave. It was the month he got tired of paying for two lives. Things started moving in the one he actually chose.",

    "Mark 9:23":
    "Every quote she asked for came back too expensive, and she had started saying so before anyone answered. Somebody pointed out that she was making the calls already braced. She tried one week of asking plainly, without the flinch in her voice, and got two prices she could work with. Those prices had probably always been there. She had been asking in a way that assumed the answer.",

    "Hebrews 11:1":
    "He bought the frame before the photograph existed. It sat empty on the shelf for most of a year and people asked about it and he said it was for something coming, which embarrassed him a little every time. When the picture finally came back from the printer it fit, because he had measured for it. The frame was not decoration. It was the first thing built.",

    "Romans 4:17":
    "She stopped saying she was trying to get out of debt and started saying she was paying off the last of it, which was not true yet by about nine thousand dollars. Her sister called it lying. She kept doing it because the old sentence made her tired and the new one made her check the account, and she checked it often. The number came down faster that year than in the three before it.",

    "Isaiah 65:24":
    "The offer was dated the Tuesday. She had prayed about it on the Thursday, two days after it was already written and sitting in somebody's drafts, and she only found that out because the recruiter mentioned the date in passing. It changed how she waited for things. She stopped picturing a request going out and started picturing something already in transit.",

    "John 16:24":
    "He complained for six years about the shifts he was given and never once asked for different ones. He had a whole case built about why it would not work. The day somebody made him say it out loud to the manager it took about forty seconds, and the manager said that was fine. He was angry for a week afterwards, at himself, about six years.",

    "Matthew 17:20":
    "She could not manage to believe the whole thing. She could believe one small piece of it, that she would make one phone call on Monday, and she believed that completely. She made the call. Then there was a slightly larger piece she could believe on Tuesday. Nobody ever handed her the whole belief at once. It arrived in the size she could actually hold.",

    "1 John 5:15":
    "After he asked, he used to keep asking, in case the first time had not gone through. Someone asked whether he would repeat an order to a waiter four times. He said no, that would be strange, you would just assume it was heard. He tried assuming it was heard. The waiting felt completely different, and it was the same waiting.",

    "Matthew 21:22":
    "She noticed she prayed in two different voices. One was for small things and it was casual and certain, and those things tended to happen. The other was for the thing she actually wanted, and it was careful and pleading and it never once sounded like she expected an answer. She started using the small voice for the big thing. It felt disrespectful for about a month.",

    "Ephesians 3:20":
    "He asked for enough to cover the month, because that felt like a reasonable thing to ask a busy God for. The month got covered, several times, always exactly. It took him years to notice that he had never once asked for the year. When he finally did, it was not harder to ask. It was the same sentence with a different number in it.",

    "Psalms 37:4":
    "She had a list of what she wanted and she worked the list like a job, and it made her miserable and none of it came. Someone told her to put the list in a drawer for a month and just enjoy Him, and she thought that was a dodge. By the end of the month two things on the list had stopped mattering and one had arrived, and she could not say which was the bigger change.",

    "Mark 10:27":
    "The number he needed was larger than anything he had earned in a year, and he kept doing the arithmetic to prove it could not be done. The arithmetic was correct every time. What he was actually proving, over and over, was that he could not do it, which nobody had disputed. The month he stopped running the numbers was the month somebody offered to run them with him.",

    "Luke 11:10":
    "She assumed there was a category of person these promises were written for and that she was outside it, and she never said that out loud because it sounded ridiculous. A woman at church asked her one day why she never asked for anything for herself. She did not have an answer. She had spent eleven years being the exception to a verse that does not list any.",

    "John 15:7":
    "He treated prayer like a service counter, somewhere he went, got seen, and left, and the asking never worked very well. The year he started staying, reading in the mornings with nothing to request, he noticed his requests had changed shape without him editing them. He was asking for different things by then, and getting most of them.",

    "Luke 1:37":
    "She kept a private list of things she had decided were too late. Her age was on it, and a language she had wanted to learn, and one relationship. She never prayed about anything on that list because it felt unfair to ask. Somebody pointed out that she had built a category God had never agreed to. She started with the language because it was the smallest, and it was not too late.",

    "James 1:6":
    "He asked on the Monday and took it back on the Wednesday and asked again on the Friday with an apology attached. He was busy the whole week. At the end of it he was exactly where he started, and tired, and he could not point to one thing he had done twice in the same direction. The problem was never effort. He had plenty of effort.",

    "Mark 5:34":
    "She had spent twelve years being told what was wrong with her by people who were paid to know. When it finally turned, the one man with the power to fix it told her it was her own doing. Nobody had handed her credit for anything in the whole twelve years. She said afterwards that the sentence did more for her than the healing.",

    "Hebrews 4:16":
    "He prayed the way he wrote emails to people he owed money. Long preamble, several apologies, the request buried near the end. Someone read one of those emails and said you sound like you are already expecting a no. He said that was just being polite. She said it is not politeness if the other person has already told you to come in.",

    "Psalms 34:10":
    "She kept an internal ranking of which needs were allowed. Rent counted. A coat that actually fit did not. She would have said God cared about her, and she would not have said He cared whether her coat fit, and she never noticed that those two sentences cannot both be true. The coat is a small story. It was not a small change.",

    "Mark 10:52":
    "Everyone around him had a reason he should keep it down, and some of them were being kind about it. He understood that they were embarrassed, and he shouted anyway, because he had worked out that this was the one afternoon it was possible and their comfort was not worth the afternoon. They were still talking when he was already being called over.",

    "1 John 3:22":
    "He read the verse and immediately went looking for the exception, because a promise that size felt like it had to have one. He found the second half, about keeping the commandments, and decided that was the catch. Years later he noticed it was not a catch at all. It described the kind of person who would be asking in the first place. He had been reading a description as a barrier.",

    "John 14:13":
    "She used to add the phrase at the end like a stamp on an envelope, and wondered why so little arrived. Someone explained that signing another person's name means you are acting for them, in the way they would act. She started asking herself what He would actually want out of what she was asking for. Some requests did not survive the question. The ones that did came in differently.",

    "James 4:3":
    "He wanted the promotion so he would stop feeling small next to his brother, and he was honest enough with himself to know it. He asked for two years. It came in the third, after the reason had quietly changed into something about the work itself, and he has wondered ever since whether those two facts are related.",

    "Luke 18:42":
    "The word he was given was not here, or granted, or done. It was receive, which is a thing you do with your hands. He thought about that for a long time afterwards, about how many things he had asked for and then stood still in front of, waiting for somebody to set them down beside him.",

    # -------------------------------------------------------- gratitude
    "1 Thessalonians 5:18":
    "The week her father was in hospital she could not thank God for the hospital, and nobody was asking her to. She thanked Him for the nurse who remembered his name, and for the parking space, and for the fact that her brother came. She said later it was not a trick to feel better. It was the only way she found to stay in the room.",

    "Psalms 100:4":
    "He used to spend the first ten minutes of prayer explaining the situation, and by the end of those ten minutes he felt worse than when he sat down. Someone suggested he open with what had already gone right that week, even if the list was short. The list was usually short. It changed the room he was praying in.",

    "Psalms 106:1":
    "She had a number in her head for how many times she could come back before it ran out. She never said the number out loud because she knew how it sounded. It was somewhere around four. She has been back a great deal more than four times now and has stopped counting, which she thinks is closer to the point than the counting ever was.",

    "Philippians 4:6":
    "He noticed his prayers and his worrying used exactly the same words in exactly the same order. The only difference was who he was facing while he did it. Putting one line of thanks at the front changed the whole thing, not because it was magic but because it turned out to be impossible to say and stay in the same posture.",

    "Psalms 103:2":
    "She started writing down what came in. Not money, just anything. It was a page a week and most of it was small. Two years later she read the first pages back and did not recognise the woman who wrote them as somebody in trouble, though at the time she was certain she was. None of it had felt like a benefit on the day.",

    "Psalms 118:24":
    "He had been treating Tuesdays as something to survive until the weekend, which meant about five sevenths of his life was a corridor. Someone pointed out that the verse does not say some days. He tried saying it on a Tuesday morning, out loud, in the car, feeling ridiculous, and kept doing it. The Tuesdays did not change. He stopped walking through them.",

    "Ephesians 5:20":
    "She could thank Him for good news easily. The test was an ordinary Wednesday with nothing in it, no occasion and no crisis either. That was the day she found out whether thankfulness was a reaction she had or a thing she did. It turned out to be a thing she did, once she practised it.",

    "Psalms 50:23":
    "He kept waiting for something to resolve so he would have a reason, and the reason never arrived on schedule. Somewhere in the second year he started praising without one. He would not claim that caused what happened next, only that he was a different man by the time it happened, and that the difference is what let him walk through it.",

    "Colossians 3:15":
    "She had always understood gratitude as a weather event, something that arrived if conditions were right. Being told to do it was strange, like being told to be tall. Then she tried it the way you try any instruction, badly and on purpose, and found it behaved much more like a muscle than like weather.",

    "Psalms 107:1":
    "He said the sentence for eleven days without meaning it, which felt dishonest, and he nearly stopped. On about the twelfth day he heard himself say it and noticed he was no longer performing. Nobody could tell him when it turned over. He is fairly sure the eleven dishonest days were not wasted.",

    "Psalms 103:1":
    "She talked to herself all day, mostly critically, and had never once thought of that running commentary as something she was allowed to direct. The psalm gave her permission to hand herself an instruction instead of a review. It felt strange in her mouth for weeks. It is the only habit from that year she still keeps.",

    "Habakkuk 3:18":
    "He wrote out everything that had not worked that year, honestly, without softening any of it, and it filled most of a page. Then he wrote the word yet at the bottom and sat there. He said afterwards that the one word was harder to write than the whole page above it, and that it was the only sentence he finished.",

    "1 Corinthians 15:57":
    "She kept thanking Him for what He was going to do, which sounds close enough but always left her standing outside of it. Somebody showed her the tense in the verse. She changed one word in how she prayed, from will give to gives, and said it was the difference between waiting at a door and being handed a key.",

    "Psalms 92:1":
    "He had always framed thanks as something owed, a bill you settle so the account stays clear, which made it a chore he did grudgingly for years. The word good in the verse undid that. He started treating it the way he treats water and sleep, as a thing taken because a person needs it, not paid because a person owes it.",

    "Psalms 118:1":
    "Her week was genuinely bad and she did not want to lie about it. Somebody showed her that the verse does not ask her to. The grounds are stated inside the verse and they are about Him. She could hold both, an honest account of the week and a true sentence about God, without either one cancelling the other.",

    "Colossians 1:12":
    "He had a running sense of being not quite qualified, in his family, at work, at church, and he had assumed the qualifying was work still ahead of him. The tense in the verse is past, and it is done to you. He read it four or five times to be sure. He calls the year after that the first year he stopped auditioning.",

    "Psalms 30:12":
    "She was grateful, genuinely, and never said any of it out loud to anyone including God, and would have told you private gratitude counts the same. The verse treats silence as the failure. She started saying one thing out loud each night to an empty kitchen. Her husband asked after a fortnight what had changed about her.",

    "Psalms 147:7":
    "He thought about being thankful a great deal, and it stayed a thought, which is to say it stayed in the same room as all his other thoughts and got outvoted daily. The first time he said it out loud in the car he was embarrassed by his own voice. It also did not get outvoted, which he had not expected.",

    "1 Chronicles 16:8":
    "She kept the good thing to herself for months because saying it felt like bragging, or like tempting something. Then a friend turned up in the same spot she had been in, and she told the story badly, in a kitchen, and watched the friend's face change. She understood then that she had been sitting on something that was not only hers.",

    "Psalms 116:17":
    "He had it the other way round for most of his life. Ask, and then thank if it came. The verse puts them in the opposite order, so he tried it, and found the asking that followed thanks was different in kind. It was shorter, for one thing. He wanted fewer things by the time he reached that part of the sentence.",

    "Luke 17:16":
    "Nine of them did exactly what they had been told to do, and nothing in the account says they were ungrateful. They were busy, and free, and on their way to the priest like He said. Only one worked out that the errand could wait. That is the whole difference between them, and it got him a sentence none of the other nine ever heard.",

    "Psalms 9:1":
    "She could praise Him with the part of her that had healthy kids and a roof. The part still angry about her mother sat out of it, every time, for years, and stayed a closed room. The verse asks for the whole thing. Bringing the angry part in did not resolve it. It did stop it being separate.",

    "Psalms 63:3":
    "David wrote that in a desert while men were trying to kill him, which is worth knowing before deciding it is a comfortable sentence. He was not comparing God to a good life. He was comparing God to being alive at all, in a week when that was genuinely in question, and he came down where he came down.",

    "Psalms 95:2":
    "He used to arrive at prayer the way you arrive at a complaints desk, with the grievance already in his hand. It was honest, and it went nowhere for a long time. Changing what he carried through the door did not make the grievance disappear. It meant he was a different man holding it by the time he set it down.",

    "Colossians 3:17":
    "She had a spiritual half of her life and an admin half, and she would have defended that split as realistic. The verse does not leave room for an admin half. She started saying thank you over the small things, the invoices and the school run, and the split closed up quietly over about a year without her deciding to close it.",

    # ------------------------------------------------------ restoration
    "Isaiah 43:25":
    "He could recite the thing he had done, word for word, fifteen years later, and had never once been asked to. He kept it like a receipt in case somebody needed proof he knew. Nobody ever asked. He was the only party to the whole matter still holding a copy, and he was holding it against himself on behalf of someone who had already thrown theirs away.",

    "Psalms 23:3":
    "She wanted to be a different woman, somebody with none of this in her history, and she prayed for exactly that for a long time. What came back was the same woman, with the same history, working again. She admits she was disappointed for about a year before she understood she had been asking to be deleted and had been given something better.",

    "2 Corinthians 5:17":
    "He kept introducing himself with the worst chapter first, to get ahead of it, so nobody could surprise him with it later. A man he respected asked him one day why he opened with something that was over. He did not have an answer. He had been keeping a thing alive by announcing it, and it had been finished for years.",

    "Lamentations 3:23":
    "She used to wake already in debt to the day before, carrying yesterday's failure into a morning that had not done anything to her. Somebody told her the supply is described as new, which means yesterday's is not what she is drawing on. It took a while to believe the morning was actually clean. She stopped starting the day owing.",

    "Isaiah 61:3":
    "He wanted to keep the ashes and get the beauty as well, which he would never have said out loud but is what he was doing. The ashes were familiar and they explained him. It is a trade, and a trade means handing something over. The hard part was never the receiving. It was letting go of the thing that had become his explanation.",

    "Revelation 21:5":
    "She had a private sorting system, things that could still be saved and things that were past it, and she only ever prayed about the first pile. The second pile she considered realism. The verse does not have a second pile. She started with one item out of it, mostly to prove a point, and it is the item she now tells people about.",

    "Isaiah 1:18":
    "He assumed there was a grading system and that he was in the lower band permanently, and that the best available outcome was being tolerated. The verse names the worst colour it can and then names the best one. No middle result is offered anywhere in the sentence. That took him longer to accept than the forgiveness did.",

    "Psalms 103:12":
    "She kept checking the same distance, the way you press a bruise, to see whether it was still there, with a sense that if she stopped checking it might come back. Somebody drew her the two directions on a napkin and showed her they never meet, at any distance, ever. She stopped pressing it that month.",

    "Isaiah 61:4":
    "He wanted to move somewhere nobody knew what had happened and start clean, and he nearly did. He stayed instead, and the work he ended up doing is work only somebody who had been through that could do. Nothing was imported. What he built came out of the exact ground that had come down.",

    "Isaiah 43:18":
    "She did not think about it constantly, which is what she would have told you. What she did was check with it before every decision, quietly, the way you check a weather app, so it got a vote in things it had no business voting on. Not remembering was never going to be possible. Not consulting it turned out to be.",

    "Psalms 51:10":
    "He had been trying to fix it himself for two years, which mostly meant managing it, keeping it out of sight, patching the same place. David does not ask for a repair. He asks for the thing to be made, out of nothing, which is a far larger request and, he found, a much easier one to make honestly.",

    "Romans 8:1":
    "She had a date in mind, unspoken, by which she would have earned the right to feel clear about herself, and the date kept moving. Somebody read her the verse and stopped at the word now and asked what she was waiting for. She could not name it. She had been serving a sentence nobody had handed down.",

    "Micah 7:19":
    "He knew the theology and could have taught it, and still went out at low tide most mornings to see whether anything had washed up. That is not a failure of belief exactly. It is a habit. Breaking the habit took far longer than believing the doctrine, and the doctrine had never been the problem.",

    "Psalms 103:5":
    "She spent a lot of time telling her kids what she used to be able to do, which was a way of visiting it. The verse puts the renewal after the filling, and she noticed she had not been filled with much for years. She changed what went in first. Some of what she had been calling age turned out to be depletion.",

    "Ezekiel 36:26":
    "He had gone hard about one particular thing and had made peace with being that way, and called it realism. He prayed for years to feel differently and nothing softened, because softening was not what was on offer. What was on offer was a removal, and when it finally came it was not gradual and it did not feel like effort.",

    "Jeremiah 30:17":
    "The word they used about her was said once, at a family thing, years ago, and it stuck the way a word does when it lands on something you already half believed. The verse quotes the word before it undoes it, which she found mattered enormously. He did not tell her to get over it. He repeated it back, and then dealt with it.",

    "1 John 1:9":
    "He asked the way you ask a favour of somebody who has already done too much for you, apologetically, half expecting to be told this was the last time. The two words in the verse are legal words. Faithful means He does it every time, and just means it would be wrong of Him not to. That is a completely different counter to walk up to.",

    "Psalms 126:4":
    "The stream by the farm was dry eleven months of the year and you could walk it like a road, and visitors assumed it had always been a road. Anyone who lived there knew what it did in the wet season, and knew a dry bed is not the same thing as no river. It is the shape of a river, waiting.",

    "Romans 4:18":
    "He never pretended the numbers were good and could recite them accurately to anybody who asked, which is why people believed him when he said it was going to work. Those two things sat side by side in him for three years without contradiction. He was not optimistic. He simply refused to build anything on the numbers.",

    "Psalms 103:3":
    "She had a category she had never brought, on the grounds that it was the one thing that was genuinely her fault and therefore outside the offer. She was reading the verse for something else entirely when the first all landed on her. There is no list of exceptions in it. She brought the thing that week.",

    "Zechariah 9:12":
    "He had been calling it stubbornness, and other people had called it worse, this refusal to give up on something long past the point where giving up would have been reasonable. The phrase in the verse names it differently. He is not free of it, he is held by it, and the verse treats that as exactly the right place to be standing.",

    "Psalms 85:6":
    "She could not find any grounds to ask, because the present offered none. So she went back through her own history and found four occasions, and wrote them down, and asked on the basis of those instead. It is a completely different prayer from the one you pray with nothing behind you. She had had the grounds the whole time.",

    "Isaiah 54:4":
    "He had assumed the forgetting was his job and that he was bad at it, and he had spent a great deal of effort trying not to think about something, which is the one instruction a mind cannot follow. The verse hands the forgetting to God and lists it as an outcome. He stopped trying to do it. Some of it went on its own.",

    "Joel 2:26":
    "The year the money finally came he ate very well and was not satisfied at all, and it frightened him, because he had assumed those were the same thing. They are listed separately in the verse for a reason. The second one arrived about four years later, and by then he could see they had never been joined the way he thought.",

    "Psalms 107:20":
    "She was braced for something dramatic, because the situation was dramatic and that seemed proportionate. What actually arrived was a sentence, in a conversation she nearly did not have, from a woman she did not know well. It did not look like an intervention at the time. It is the thing everything after it moved on.",
}

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


def build_paragraphs(bible, raw, card_ref):
    """Normalise paragraphs and resolve their inline scripture anchors.

    A paragraph is either a plain string or a dict with text and links. A link
    names a phrase inside that paragraph and the biblical moment it touches. The
    phrase has to appear in the text exactly once, or the build stops: a link the
    app cannot find would silently vanish from the story.

    The same links become the parables listed at the end, so a moment is written
    once and shows up in both places.
    """
    paras, parables, seen = [], [], set()

    for para in raw:
        if isinstance(para, str):
            paras.append({"text": para, "links": []})
            continue

        text, out = para["text"], []
        for link in para.get("links", []):
            phrase = link["phrase"]
            n = text.count(phrase)
            if n != 1:
                raise SystemExit(
                    "%s: the phrase %r appears %d times in its paragraph, needs exactly 1"
                    % (card_ref, phrase, n))
            book, chap, first, last, vtext = lookup(bible, link["ref"])
            entry = {
                "phrase": phrase,
                "ref": link["ref"],
                "book": book, "chapter": chap, "verse": first,
                "moment": link["moment"],
                "text": vtext,
            }
            out.append(entry)
            if link["ref"] not in seen:
                seen.add(link["ref"])
                parables.append(entry)

        paras.append({"text": text, "links": out})

    return paras, parables


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
        # Three sources, newest shape first. Everything ends up as paragraphs
        # plus parables so the app only has to understand one shape.
        if ref in FULL:
            f = FULL[ref]
            paras, parables = build_paragraphs(bible, f["paragraphs"], ref)
            card["story"] = {
                "badge": "Parable",
                "paragraphs": paras,
                "parables": parables,
                "full": True,
            }
        elif story:
            card["story"] = {"badge": story[0],
                             "paragraphs": [{"text": story[1], "links": []}],
                             "parables": [], "full": False}
        elif ref in EXTRA_STORIES:
            card["story"] = {"badge": "Parable",
                             "paragraphs": [{"text": EXTRA_STORIES[ref], "links": []}],
                             "parables": [], "full": False}
        streams.setdefault(stream, []).append(card)

    out = {
        "translation": "King James Version",
        "license": "public domain",
        "streams": streams,
    }
    with io.open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    shortest = min(len(v) for v in streams.values())
    todo = []
    for name in ("receive", "gratitude", "restoration"):
        cards = streams.get(name, [])
        full = [c for c in cards if c.get("story", {}).get("full")]
        todo += [(name, c["ref"]) for c in cards if not c.get("story", {}).get("full")]
        print("%-12s %2d cards, %2d written to full length, %2d still short"
              % (name, len(cards), len(full), len(cards) - len(full)))

    allcards = [c for v in streams.values() for c in v]
    words = sum(len(p["text"].split()) for c in allcards for p in c["story"]["paragraphs"])
    words += sum(len(pb["moment"].split()) for c in allcards for pb in c["story"]["parables"])
    anchors = sum(len(p["links"]) for c in allcards for p in c["story"]["paragraphs"])
    print("%d inline scripture anchors" % anchors)
    print("\n%d days before anything repeats, %s words of story -> %s"
          % (shortest, "{:,}".format(words), OUT))
    if todo:
        print("still short (%d of %d)" % (len(todo), sum(len(v) for v in streams.values())))


if __name__ == "__main__":
    main()
