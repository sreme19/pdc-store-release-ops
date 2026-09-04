#!/usr/bin/env python3
"""Builds the competitor Play Store audit HTML report from curated data."""
import html
import os

OUT_DIR = "/Users/performek5/Desktop/Code/pdc-store-release-ops/research/competitor-play-store-audit"

def esc(s):
    return html.escape(s, quote=False)

# ---------------------------------------------------------------------------
# Per-app data (curated from raw-notes/*.md, written 2026-09-02)
# ---------------------------------------------------------------------------
APPS = [
    # ---------------- GLOBAL MAINSTREAM ----------------
    dict(
        slug="tinder", name="Tinder — Match. Chat. Date.", group="Global mainstream swipe apps",
        package="com.tinder", developer="Tinder LLC", rating="4.2", reviews="9.16M",
        installs="500M+", monetization="Ads, In-app purchases", content_rating="18+",
        badge="#2 top free dating", updated="Aug 31, 2026",
        short_desc="The dating app that does it all - make friends, meet people, or find a date",
        summary="Opens with three emoji-bracketed hook lines and a huge social-proof number (60 billion matches to date), positioning itself as the world's most popular free dating app across 190 countries. Explains the swipe mechanic as a trademarked concept (Swipe Right™ / Swipe Left™) and structures its Plus/Gold premium tiers as a clear feature ladder. Emoji appear on almost every line as a scanning aid. Closes with a long, formal subscription auto-renewal disclosure and a one-line disclaimer that photos are of models.",
        whats_new="Generic forward-looking copy about improving how users find and connect — no specific feature named.",
        shots=[
            ("screenshot-1.jpg", "“It starts with a swipe” — full-bleed couple photo, bold white headline low on the frame."),
            ("screenshot-2.jpg", "“Attract people who actually get you” — same red-overlay lifestyle-photo template."),
            ("screenshot-3.jpg", "“First dates hit different with friends” — pink background, a “Double Date” feature badge floating over a testimonial-style photo grid."),
            ("screenshot-4.jpg", "“Connect with confidence” — verified-badge UI callout layered over a portrait photo."),
            ("screenshot-5.jpg", "Continues the identical template: dark photo background, bold white headline, small floating UI-proof badge."),
        ],
        aso=[
            "Title keyword-stacks the exact verbs users search for: “Match. Chat. Date.”",
            "Subtitle deliberately widens past romance (“make friends, meet people, or find a date”) to broaden the install funnel.",
            "Google's own “#2 top free dating” rank badge does credibility work the description doesn't have to.",
            "Every screenshot uses one template — full-bleed lifestyle photo, bold headline, small real-feature proof badge — brand photography first, feature proof second.",
            "Heavy legal/subscription disclosure is pushed to the very bottom, after all persuasive copy.",
        ],
    ),
    dict(
        slug="bumble", name="Bumble: Dating App & Friends", group="Global mainstream swipe apps",
        package="com.bumble.app", developer="Bumble Holding Limited", rating="4.2", reviews="1.6M",
        installs="100M+", monetization="In-app purchases (Boost, Premium, Spotlight, SuperSwipe)",
        content_rating="18+", badge="#1 top grossing dating", updated="Sep 1, 2026",
        short_desc="The dating app to meet new people, chat and date with singles or make friends!",
        summary="Leads with its core differentiator (women message first) inside a heavily sectioned description with bolded sub-headers and emoji-led bullets on nearly every line. Explicitly keyword-stacks identity terms (“gay dating app,” “bisexual dating app,” “Christian dating app,” “Jewish dating app”) for long-tail search capture, then closes by naming its corporate siblings (Badoo, Fruitz).",
        whats_new="No dated changelog block; an always-on “Advanced Filters help you connect based on goals, plans, and more” callout is shown instead.",
        shots=[
            ("screenshot-1.jpg", "Full-bleed lifestyle photo of a couple, warm backlit grade, bold yellow “MAKE THE FIRST MOVE™” headline — pure brand/emotion, no UI."),
            ("screenshot-2.jpg", "Device-framed UI shot of the Advanced Filters screen on a solid Bumble-yellow field, black condensed headline “FIND YOUR PERSON.”"),
            ("screenshot-3.jpg", "Device-framed match-confirmation screen (“What a match!”) with an opening-message prompt, headline “START THE CHAT.”"),
            ("screenshot-4.jpg", "Device-framed profile-detail card using an Indian name (“Rahul, 27”) with floating heart/chat badges, headline “STAND OUT MORE” — localized for the India store."),
            ("screenshot-5.jpg", "Device-framed onboarding/interest-picker screen, pale-yellow field, headline “CONNECT OVER INTERESTS.”"),
        ],
        aso=[
            "Title packs two intents (“Dating App” + “Friends”) into one string to capture both romantic and platonic search traffic.",
            "Storytelling order is emotion → proof → feature: one warm hero photo, then four UI screenshots once attention is captured.",
            "High-contrast brand palette (yellow + black) is identical across every screenshot and the icon — strong thumbnail-size recall in search results.",
            "Leans on the Play Store's own “#1 top grossing” badge instead of baking install numbers into the copy.",
            "Screenshot 4 swaps in an Indian name and setting — real India-store localization, not a generic Western cast.",
            "Monetization is disclosed by naming every paid product specifically (Boost, Premium, Spotlight, SuperSwipe) rather than vaguely.",
        ],
    ),
    dict(
        slug="hinge", name="Hinge Dating App: Match & Date", group="Global mainstream swipe apps",
        package="co.hinge.app", developer="Hinge, Inc.", rating="4.0", reviews="477K",
        installs="10M+", monetization="In-app purchases (Hinge+, HingeX)", content_rating="18+",
        badge="#3 top grossing dating", updated="Aug 28, 2026",
        short_desc="The Dating App Designed to be Deleted | Match, Flirt, Meet & Date Single People",
        summary="Builds the entire listing around one brand joke — “designed to be deleted” — repeated in the description, a dedicated “HOW WE GET YOU OFF HINGE” section, and even the What's New changelog. Emoji use is light and restrained. Uniquely among the set, it quotes three press outlets (Daily Mail, Washington Post, TechCrunch) as third-party social proof, and discloses subscription auto-renewal terms in a distinct, legally thorough block.",
        whats_new="Keeps the brand joke alive: “We made performance improvements which means you may end up deleting our app even sooner than you intended.”",
        shots=[
            ("screenshot-1.jpg", "Full-bleed editorial photo of a couple talking outdoors, serif headline “You never know where a date will take you” — no UI shown at all."),
            ("screenshot-2.jpg", "Collage of circular verified-badge headshots (diverse, real-looking), serif headline “Show up as you are and see what happens.”"),
            ("screenshot-3.jpg", "Device-framed profile screen showing named Dating Intentions (“Looking for something serious and silly”), headline “Start on the same page.”"),
            ("screenshot-4.jpg", "Device-framed Voice Prompt profile card with a playable audio waveform, headline “Get a sense of who they are.”"),
            ("screenshot-5.jpg", "Device-framed in-app chat mixing text and voice-note bubbles, headline “Easily strike up conversations.”"),
        ],
        aso=[
            "A single brand tagline is reused consistently across the subtitle, the full description, and the What's New text — the strongest cross-surface brand-voice consistency seen in the set.",
            "Only listing to use third-party press quotes as explicit social proof, rather than store-badge numbers alone.",
            "Screenshots open with real-photo/verified-people imagery to sell trust before any product screen.",
            "Serif display typography signals an editorial, premium tone — distinct from competitors' bold sans-serif marketing type.",
            "Every named feature in the copy (Dating Intentions, Voice Prompts, Prompts) has a matching, clearly labeled screenshot.",
            "Unusually transparent — “all photos are of models” disclaimer sits oddly next to a “real, verified people” narrative.",
        ],
    ),
    dict(
        slug="happn", name="happn: dating app", group="Global mainstream swipe apps",
        package="com.ftw_and_co.happn", developer="happn", rating="4.2", reviews="2.07M",
        installs="100M+", monetization="Ads, In-app purchases", content_rating="18+",
        badge="#8 top free dating", updated="Sep 1, 2026",
        short_desc="happn is the real-life dating app where you date and meet people!",
        summary="Opens with a four-word tagline (“Like - Crush - Chat - Date”) then a magazine-style narrative built around its differentiated hook — real-life geo-proximity (“crossing paths”), not blind swiping. Introduces proprietary capitalized feature names (Teasers, CrushTime, SuperCrush) that double as ownable brand vocabulary. No emoji, no explicit pricing disclosure.",
        whats_new="Announces a new “Hobbies” feature with playful example tags for showing personality and matching on shared interests.",
        shots=[
            ("screenshot-1.jpg", "Dark background, serif headline “Find your Crush,” tilted device mockup of a real profile card with a “350 mi away” distance tag."),
            ("screenshot-2.jpg", "Same dark template, “...or a new friend” — profile card shows “Friendship / Hangout” intent tags, broadening beyond romance."),
            ("screenshot-3.jpg", "“Make it happn!” — match-celebration interstitial over colorful abstract shapes."),
            ("screenshot-4.jpg", "Light cream background, literal map UI with clustered pins visualizing the proximity mechanic — “Find the people you cross paths with.”"),
            ("screenshot-5.jpg", "SuperCrush upsell interstitial over abstract geometric color blocks."),
        ],
        aso=[
            "Core differentiator (real-life proximity) is reinforced consistently in both description section headers and a dedicated map-UI screenshot — a clear unique-mechanic narrative.",
            "Proprietary named features (Crush, SuperCrush, Teasers, Hobbies) function as ownable, repeatable keywords.",
            "Two-toned visual system (dark serif slides, then light sans-serif slides) still reads as one brand thanks to consistent doodle accents and device-frame angle.",
            "Weaker category rank (“#8”) than Tinder/Bumble/Hinge, but still carries a Google-granted badge.",
            "Reviews sampled skew negative on premium-paywall frustration and forced Google Sign-In — a reputation risk regardless of listing polish.",
        ],
    ),
    dict(
        slug="okcupid", name="OkCupid: Online Dating App", group="Global mainstream swipe apps",
        package="com.okcupid.okcupid", developer="Match Group Americas, LLC", rating="3.9", reviews="685K",
        installs="50M+", monetization="Ads, In-app purchases", content_rating="18+",
        badge="none observed", updated="Aug 14, 2026",
        short_desc="Find your kind of love on OkCupid! Meet singles online and go on great dates!",
        summary="Six or seven plain-prose paragraphs of personality-first brand positioning come before any bullet list, with repetitive phrasing (“local dating,” “meet new people,” “great dates”) that reads as deliberate SEO keyword-stuffing rather than persuasive copy. Explicitly calls out India and LGBTQ+ inclusivity as differentiators. Closes with a three-quote press block.",
        whats_new="No distinct changelog text was surfaced separately from the description on this listing.",
        shots=[
            ("screenshot-1.jpg", "Flat vector illustration on magenta, “GO ON GREAT DATES,” a ribbon stat callout “195 MILLION MATCHES EACH YEAR.”"),
            ("screenshot-2.jpg", "Device-framed UI on royal blue: “FIND LOCAL SINGLES” with an India-localized profile (“Aakash, 28, Indira Nagar, Bengaluru”)."),
            ("screenshot-3.jpg", "Device-framed compatibility-questionnaire UI, “ANSWER FUN QUESTIONS,” showing a 91% match score."),
            ("screenshot-4.jpg", "Device-framed browsing UI mirroring slide 2's layout with another India-localized profile (“Maya, 28, Colaba, Mumbai”)."),
            ("screenshot-5.jpg", "In-app chat referencing a specific personality detail, illustrating “personality-first” matching."),
        ],
        aso=[
            "The only listing whose screenshots themselves — not just the description — show Indian names, cities, and photos; the strongest visible India-localization signal in the whole set.",
            "Strict two-colour alternating background system (magenta/blue) gives strong brand consistency but a busier feel than photography-led carousels.",
            "No category rank badge and no numeric pricing disclosure, unlike higher-ranked peers.",
            "Reviews sampled show a high-severity billing/reliability complaint pattern (charged-but-inaccessible premium features) sitting under an otherwise mid-pack 3.9 rating.",
        ],
    ),
    dict(
        slug="badoo", name="Badoo Dating App: Meet & Date", group="Global mainstream swipe apps",
        package="com.badoo.mobile", developer="Badoo", rating="3.7", reviews="6.65M",
        installs="100M+", monetization="Ads, In-app purchases", content_rating="18+",
        badge="none observed", updated="Sep 1, 2026",
        short_desc="Chat and date or make friends! Meeting people is easier than other dating apps.",
        summary="Deliberately broad positioning (“you do you” covers fun dates, long-term relationships, and casual chats in one sentence). No emoji in the body; four hyphen-bulleted sections cover perks, features, Premium Plus perks (the only starred section), and a detailed safety section (photo verification, “private detector,” “rude message detector”). Explicitly discloses Bumble Inc. as its parent company.",
        whats_new="No distinct changelog text was surfaced on this pull.",
        shots=[
            ("screenshot-1.jpg", "Solid lavender field, red “Date with confidence” headline over a 2x2 grid of real-looking couple photo cutouts — pure brand imagery, no UI."),
            ("screenshot-2.jpg", "Device-framed “Encounters” swipe screen with a verified profile and a “Liked you” pill."),
            ("screenshot-3.jpg", "Device-framed “Discover” feed showing a profile with hashtag interest tags and a visible pay-to-message credit cost (“250”) — an unusually transparent monetization cue at the ASO layer."),
            ("screenshot-4.jpg", "In-app chat transitioning into an incoming video-call overlay."),
            ("screenshot-5.jpg", "Encounters card with floating interest-tag chips (“Dog Lover,” “90s HipHop”)."),
        ],
        aso=[
            "Safety messaging gets its own detailed, named-feature section (photo verification, rude-message detector) — more specific than most competitors' generic safety claims.",
            "Openly names its corporate parent (Bumble Inc.) and sibling apps — a transparency move no other listing in the set makes.",
            "The only screenshot carousel to expose a literal paywall mechanic (a coin-cost badge) before install — transparent, but also surfaces the paywall pre-emptively.",
            "Reviews sampled show a recurring “free-to-download but pay-to-use” sentiment gap against the “free dating app” framing repeated in the description.",
        ],
    ),
    dict(
        slug="coffeemeetsbagel", name="Coffee Meets Bagel Dating App", group="Global mainstream swipe apps",
        package="com.coffeemeetsbagel", developer="Coffee Meets Bagel Pte. Ltd.", rating="3.2", reviews="125K",
        installs="5M+", monetization="In-app purchases", content_rating="18+",
        badge="Editors' Choice", updated="Aug 24, 2026",
        short_desc="The dating app for serious daters - Match, meet new people & date with singles",
        summary="Front-loads three arrow-bulleted hook lines and a strong stat (“91% of our daters are looking for a serious relationship”) before any narrative copy. Four purple-heart-bulleted feature sections use benefit-oriented sentences rather than terse bullets. A named “MEET CMB PREMIUM” section quantifies value (“up to 2x more dates”) without pricing. Closes with quotes from Yahoo Finance, Mashable (x2), and Women's Health.",
        whats_new="Names three specific features: “Topic Suggestions” (AI first-message prompts), “Headlines” (a personality tagline), and “Real Dates” (first-date idea suggestions).",
        shots=[
            ("screenshot-1.jpg", "Full-bleed city-street lifestyle photo of a couple, white headline “Date for something real.”"),
            ("screenshot-2.jpg", "Full-bleed beach lifestyle photo, decorative gradient hearts, “Ready to date for something real?”"),
            ("screenshot-3.jpg", "Device-framed Suggested-feed UI on lavender: profile card with ID Verified / Selfie Verified badges and a “Sarah liked you and replied” snippet."),
            ("screenshot-4.jpg", "Device-framed profile-editing screen with detailed fields (education, prompts, verification badges) — “Say more in a few words.”"),
            ("screenshot-5.jpg", "Device-framed Suggested feed with pre-written, editable icebreaker CTAs (“Send flowers,” “Send like”)."),
        ],
        aso=[
            "“Editors' Choice” badge substitutes for a numeric rank — likely a stronger trust signal since it's a curated Google distinction, not a leaderboard position.",
            "A specific stat (91%) plus a cumulative usage number (150M matches) plus named press quotes stack three different social-proof types in one description.",
            "Screenshots repeatedly surface “ID Verified” / “Selfie Verified” badges directly on profile cards — a visual trust signal reinforcing the “safe place to meet” claim, not just an assertion in text.",
            "Notably the lowest rating in the set (3.2) despite the curated badge and premium visual polish — reviews cite pricing complaints and slow match delivery, a reminder that ASO polish and review sentiment can diverge sharply.",
        ],
    ),
    # ---------------- INDIA-FOCUSED MODERN DATING ----------------
    dict(
        slug="aisle", name="Aisle - Dating App For Indians", group="India-focused modern dating",
        package="com.aisle.app", developer="Aisle Network Pvt. Ltd.", rating="4.6", reviews="459K",
        installs="10M+", monetization="Ads, In-app purchases (Plus / Premium / Concierge tiers)",
        content_rating="18+", badge="none observed", updated="Aug 27, 2026",
        short_desc="Built for real commitment",
        summary="Opens with a numeric hook (“2.2M success stories”) and self-labels as “the first date-to-marry app,” positioning between casual swipe apps and pure matrimony sites. No emoji; polished, editorial startup-brand voice. Explicitly and transparently names and describes each paid tier with auto-renewal terms — the most transparent monetization disclosure in the set. A distinct “In the Press” section links four outlets (Inc42, Deccan Chronicle, YourStory, Social Samosa), and it closes by naming its parent, Info Edge (India) Ltd. — the company behind Naukri, Jeevansathi, and 99acres — to borrow trust.",
        whats_new="Generic: “Bug fixes and user experience improvements.”",
        shots=[
            ("screenshot-1.jpg", "Lifestyle rooftop photo, “aisle” wordmark, and a stat-badge row baked directly into the first frame: “4.5 Rating,” “20M+ Members,” “9K Matches/day.”"),
            ("screenshot-2.jpg", "Paired his/hers lifestyle photo, headline “India's first date-to-marry app.”"),
            ("screenshot-3.jpg", "Device-framed Discover-tab UI on magenta gradient: a verified profile with a text-prompt response and a “Comment” icebreaker button — “Connect with verified profiles.”"),
            ("screenshot-4.jpg", "Device-framed “Concierge” premium feature UI showing 10,000+ handpicked members — a paid feature tied directly to its own screenshot."),
            ("screenshot-5.jpg", "Device-framed profile with a text-prompt icebreaker card — “Start conversations with icebreakers.”"),
        ],
        aso=[
            "Positions in a deliberate middle ground — “Dating App For Indians” + “Built for real commitment” — signaling geography and anti-casual intent without using “matrimony,” directly relevant to how a dating-coach-branded app might differentiate from pure swipe apps.",
            "Bakes rating, member count, and daily-match count into the very first screenshot as a persistent stat row — the value proposition is scannable in the single frame most likely to be seen in search thumbnails.",
            "Real device-frame chrome (bezel, notch, side buttons) gives a more “authentic modern app” feel than the matrimony apps' borderless marketing-card style.",
            "Every named feature in the text (Comments, Concierge, Private Browsing, Advanced Filters) has a matching, clearly labeled screenshot — tight text-to-visual consistency.",
            "Highest rating in the whole set (4.6), yet sampled negative reviews repeat the same “matches dry up after payment” pattern seen across matrimony apps — a category-wide weak point.",
            "No visible developer replies to negative reviews — a reputation-management gap versus the matrimony apps, which reply to nearly everything.",
        ],
    ),
    dict(
        slug="quackquack", name="QuackQuack Dating App in India", group="India-focused modern dating",
        package="com.quackquack", developer="QuackQuack.in", rating="4.3", reviews="703K",
        installs="10M+", monetization="Ads, In-app purchases", content_rating="18+",
        badge="none observed", updated="Sep 1, 2026",
        short_desc="Dating app to meet, chat, find friends easier than other dating apps in India.",
        summary="No emoji anywhere. Plain, long-form paragraphs narrate the whole user funnel (create profile → browse/filter by city and interests → like/chat → an optional human-matchmaker feature → meet offline), name-dropping specific Indian cities for local SEO. Trust/safety messaging (phone/email verification, moderation, fake-profile removal) is unusually prominent — a direct answer to India-market skepticism about dating-app authenticity.",
        whats_new="“Improvements for speed and reliability” — generic.",
        shots=[
            ("screenshot-1.jpg", "“Meet Awesome People” — mustard-yellow background, brush-stroke-highlight headline, social-proof strap line “40 Million Users — India's Fastest Growing Dating App.”"),
            ("screenshot-2.jpg", "“Match” — device-framed swipeable profile card with verification badges and Skip/Like buttons."),
            ("screenshot-3.jpg", "“Make New Friends” — device-framed list view (“New and online (9815)”) emphasizing active-user volume."),
            ("screenshot-4.jpg", "“Date” — device-framed “Visitors” grid reinforcing reciprocal-interest visibility."),
            ("screenshot-5.jpg", "“Chat” — device-framed real chat thread arranging a coffee meetup."),
        ],
        aso=[
            "Title keyword-stacks “Dating App” + “India” directly for high-intent local search rather than a brand-only title.",
            "Screenshot sequence tells a literal funnel story (Meet → Match → Make Friends → Date → Chat) using real UI, trading emotional aspiration for credibility.",
            "Distinctive brand color system (mustard yellow + black/white brush-stroke text) creates strong shelf differentiation against the red/pink-dominated category.",
            "Large, repeated social-proof numbers (39M/40M users) anchor both the description and the first screenshot's overlay text.",
            "Description is thorough but the least scannable in the set — no emoji or bullet aids despite being one of the longest.",
        ],
    ),
    dict(
        slug="frnd", name="FRND: Talk to Friends Online", group="India-focused modern dating",
        package="com.dating.for.all", developer="FRND", rating="4.5", reviews="577K",
        installs="50M+", monetization="In-app purchases", content_rating="12+",
        badge="#10 top free social", updated="Aug 26, 2026",
        short_desc="Live Audio & Video Calling App To Connect With Friends, Meet Online & Play Game",
        summary="Opens in Hinglish (“Boring life ko bolo tata bye-bye 👋 aur FRND pe naye dosto ko kaho Hi ♥️”) — the most India-vernacular hook in the whole set, at extremely high emoji density throughout. Frames itself as friendship/social first despite a package id (com.dating.for.all) that suggests a dating-category origin. Lists 12 supported Indian regional languages and layers in creator-economy mechanics (become an “RJ,” earn rewards, virtual gifts) absent from every pure dating app reviewed.",
        whats_new="Generic bullets: “Faster, smoother calls,” “Bug fixes (goodbye glitches).”",
        shots=[
            ("screenshot-1.jpg", "Magenta background, flat cartoon-avatar friend-network diagram — “Your New Social Circle,” no real photography anywhere."),
            ("screenshot-2.jpg", "Device-framed discovery/room-browsing UI with cartoon-avatar tiles and a coin balance — “Stay Anonymous, Share Freely.”"),
            ("screenshot-3.jpg", "Device-framed icebreaker/game UI with a “Love Meter” and a multiple-choice question — “Chat About What You Love!”"),
            ("screenshot-4.jpg", "Device-framed language-selection screen showing 11+ regional scripts — “Make FRNDs in Your Own Language.”"),
            ("screenshot-5.jpg", "3D cartoon safety mascot over a dimmed screenshot with three checkmarked safety-feature chips — “Women Safety, Our Priority.”"),
        ],
        aso=[
            "The most India-localized ASO approach in the set: Hinglish copy from line one, a 12-language feature list, and a dedicated language-picker screenshot.",
            "An anonymity-first, no-real-photos visual identity (flat cartoon avatars throughout) directly supports its “hide your face, still connect” positioning — relevant if a lower-friction, less photo-dependent onboarding path is ever worth exploring.",
            "“Women Safety” gets its own dedicated screenshot with a mascot + checklist — a more visual, concrete trust treatment than competitors' paragraph-only safety copy.",
            "Lower content rating (12+) than every dating app in the set, reflecting its friendship-first positioning and likely widening its addressable install base.",
        ],
    ),
    # ---------------- INDIA MATRIMONY / MARRIAGE-INTENT ----------------
    dict(
        slug="shaadicom", name="Shaadi.com Matrimony App", group="India matrimony / marriage-intent",
        package="com.shaadi.android", developer="People Interactive", rating="4.4", reviews="475K",
        installs="10M+", monetization="Freemium (premium subscription plans upsold in-listing)",
        content_rating="18+", badge="none observed", updated="Aug 31, 2026",
        short_desc="India's most trusted matrimony & marriage app - 30 years of matchmaking legacy",
        summary="Opens with an emoji-laden hook and immediately stacks social-proof numbers (35 million members, 8 million marriages, 30 years) before explicitly disavowing “casual dating” and “swiping.” The body is organized into clearly emoji-labeled sections, then a long SEO tail covering every religion, community, regional language, NRI country, and city — plus an “Also known as” block of common misspellings purely for search-match capture. Repeats its three core stats a second time as a closing hook.",
        whats_new="Generic stability/performance message — no feature-specific changelog.",
        shots=[
            ("screenshot-1.jpg", "Lifestyle photo, sunlit forest, red/white headline “India's OG Matchmakers / for 30 years.”"),
            ("screenshot-2.jpg", "Paired lifestyle photo (his/hers), “Install & Message for Free.”"),
            ("screenshot-3.jpg", "Solid-red feature card: “Highest rated matrimony app in India,” a 4.4★/5L-reviews badge plus stacked testimonial quotes."),
            ("screenshot-4.jpg", "Red card, “80% profiles are multi-verified,” a verified profile photo with AI/Phone/Selfie-verified pill badges."),
            ("screenshot-5.jpg", "Red card, “100% privacy and contact filters,” a blurred phone-call photo with a padlock icon and masked contact fields."),
        ],
        aso=[
            "Title stays brand-only — all keyword stacking (every religion, caste, region, NRI country, city, and misspelling) is pushed into the long-tail description instead.",
            "Social-proof numbers are bracketed at both the top and bottom of the description — a deliberate repetition technique.",
            "Explicitly anti-positions against “dating apps” (“No casual dating. No swiping.”) to reassure a marriage-seeking, family-oriented audience.",
            "Verification and privacy are the two most emphasized trust mechanics in both copy and screenshots — a direct answer to the “fake/bot profile” complaint visible in its own reviews.",
            "Developer replies to nearly every visible negative review within a day, using the reviewer's first name — a visible, personalized reputation-management habit.",
        ],
    ),
    dict(
        slug="bharatmatrimony", name="Bharat Matrimony® Marriage App", group="India matrimony / marriage-intent",
        package="com.bharatmatrimony", developer="Matrimony.com Ltd.", rating="4.0", reviews="193K",
        installs="10M+", monetization="Freemium (Prime/premium membership for chat, calls, photo/number unlock)",
        content_rating="18+", badge="none observed", updated="Jul 28, 2026",
        short_desc="Biggest Matrimony & Shaadi App for Indians from Matrimony.com Group",
        summary="Opens in all-caps with a direct authority claim, then doubles the opening in Hindi (Devanagari script) — a bilingual structure not seen anywhere else in the set. No emoji at all; all-caps section headers replace them. The misspelling-capture tactic is unusually overt, calling out “sometimes misspelled as Bharath or Barath” directly inline rather than burying it in a footer. Cross-promotes the wider Matrimony.com portfolio of language- and community-specific apps at the end.",
        whats_new="Minimal: “Bug Fixes and Performance Enhancements.”",
        shots=[
            ("screenshot-1.jpg", "A 3x3 grid of named real “success story” couple photos with stat callouts: “26 Years,” “4 Crore+ Customers Served.”"),
            ("screenshot-2.jpg", "Mother/daughter lifestyle photo with an in-hand phone showing a Hindi language toggle — “Bharat Matrimony now available in Hindi too.”"),
            ("screenshot-3.jpg", "Genuine in-app match-list UI (tabs, match count, verification badges, bottom nav) — the most literal, detailed UI screenshot of any matrimony app reviewed."),
            ("screenshot-4.jpg", "Genuine horoscope/kundli-matching UI with real astrology-chart fields — an India-specific feature given its own dedicated screenshot."),
            ("screenshot-5.jpg", "A blurred profile photo behind an “Upgrade to view photo” CTA — ties privacy messaging directly to the paywall mechanic."),
        ],
        aso=[
            "The only listing with a bilingual English+Hindi description block right at the top — a distinctive India-localization signal, reinforced by a dedicated “now in Hindi” screenshot.",
            "Opens its screenshot carousel with a named-couples testimonial grid rather than stock photography — leans into authenticity immediately.",
            "Shows genuine, detailed in-app UI (real nav bars, buttons, match counts) more than any other matrimony listing, at the cost of a less polished/branded look.",
            "A privacy/paywall coupling shown very literally on-screen (blurred photo + upgrade CTA) is more transparent about the monetization mechanic than Shaadi.com's more abstract framing.",
            "Lower rating (4.0) than Shaadi.com (4.4) on a similar install base; sampled reviews repeat the same “profile flow dries up post-payment” complaint pattern.",
        ],
    ),
    dict(
        slug="betterhalf", name="Betterhalf.ai® - Matrimony App", group="India matrimony / marriage-intent",
        package="com.betterhalf", developer="Betterhalf®", rating="4.0", reviews="35.8K",
        installs="5M+", monetization="In-app purchases (premium membership, 24h boost, visibility badges)",
        content_rating="18+", badge="none observed (categorized as “Social,” not “Dating”)", updated="Sep 18, 2025",
        short_desc="Indian Matchmaking & Matrimony App. Find Genuine & Verified Profiles for Shaadi.",
        summary="A sequence of short, bolded section headers (“Find matrimony profiles by religion,” “...by mother tongue,” “...from top Indian cities”) reframes a faceted-search feature list as SEO copy. Virtually no emoji; plain, transactional tone. Named castes, religions, languages, and cities are exhaustively enumerated. Embeds hard numbers directly in the copy (“20 lakhs verified profiles, 2 lakh+ relationships, 15,000+ marriages”) and cross-sells adjacent services (astrologer, wedding planning, love coach) to position itself as a full wedding-journey platform.",
        whats_new="Not visible as a distinct section on this pull — also the oldest “Updated on” date of any app reviewed (Sep 2025).",
        shots=[
            ("screenshot-1.jpg", "Landscape collage of small real wedding-couple photos with a duotone overlay, banner “MET ON BETTERHALF” and “20,000+ couples.”"),
            ("screenshot-2.jpg", "Landscape marketing graphic: a rendered hand holding a phone showing a selfie-verification camera UI — “Selfie Verified Profiles.”"),
            ("screenshot-3.jpg", "Landscape graphic: two illustrated profile cards linked by a heart icon, banner “GUARANTEED” — “Compatible Connections.”"),
            ("screenshot-4.jpg", "Landscape graphic: a couple's faces cropped into a heart shape, floating compatibility-filter tags (Language, Income, Food Habits) — “Helping You Find Better Love.”"),
            ("screenshot-5.jpg", "Landscape graphic: a young couple with playful chat-bubble callouts — “Designed for the New Generation.”"),
        ],
        aso=[
            "Title and subtitle both foreground “Matrimony” over “Dating,” and the app sits in Google's “Social” category rather than “Dating” — a deliberate distancing from casual-dating connotations.",
            "The most aggressive keyword-stacking in the set (religion, caste, mother tongue, city, all enumerated) at a real cost to prose readability.",
            "Every screenshot is an illustrated/composited marketing graphic — none are literal device-framed UI captures, so a prospective installer sees zero real app screens before installing, unlike every other app profiled.",
            "Landscape-orientation screenshots render smaller and more compressed inside Play's mobile carousel strip than the portrait phone-mockup style everyone else uses.",
            "No category rank badge is shown — worth noting since a rank badge is a low-effort, high-visibility trust signal other apps in this set benefit from.",
            "Cross-sells adjacent services (astrology, wedding planning, love coach) — a differentiated retention/monetization angle beyond pure matchmaking.",
        ],
    ),
    dict(
        slug="knot", name="Knot.dating - AI Matrimony", group="India matrimony / marriage-intent",
        package="com.knotdating.live", developer="Knot Dating", rating="4.1", reviews="598",
        installs="10K+", monetization="Not disclosed via store badges (invite-only, verification-gated)",
        content_rating="18+", badge="none observed", updated="Aug 23, 2026 (v1.0.49)",
        short_desc="Trusted matrimony & matchmaking app for serious relationships",
        summary="Opens with “Tired of casual dating? Now tie the Knot,” immediately claiming “India's first AI-powered conversational matchmaking experience” against rigid-filter matrimony platforms. No emoji; clean, aspirational, editorial tone. Since it can't yet compete on scale (598 reviews, 10K+ installs, no rank badge), it substitutes founder-pedigree social proof (“Founded by Shark Tank-backed entrepreneurs”) for install/rating numbers, and discloses no subscription pricing anywhere.",
        whats_new="Generic: “Bug fixes and performance improvements for a smoother app experience.”",
        shots=[
            ("screenshot-1.jpg", "A modern Indian bride and groom in wedding attire wearing sunglasses; headline “Tired of dating? Now tie the Knot” + “India's First AI Matchmaker.”"),
            ("screenshot-2.jpg", "Genuine identity-verification/selfie-liveness screen — “100% Verified Profiles.”"),
            ("screenshot-3.jpg", "Genuine match/home feed with matrimony-style bio fields (community, education) and an AI “Why is this match good for you?” explanation prompt."),
            ("screenshot-4.jpg", "Genuine “Meet your match!” reveal screen with both users' avatars side by side."),
            ("screenshot-5.jpg", "Genuine onboarding step offering an AI phone call to auto-build the user's profile from a biodata upload."),
        ],
        aso=[
            "Title stacks both “dating” and “matrimony” intent keywords in one string, surfacing for marriage-minded searches a pure “dating app” title would miss.",
            "Leads its very first screenshot with an unambiguous positioning claim (“India's first AI Matchmaker”) to compensate for a tiny review base versus the scale leaders in this set.",
            "Foregrounds real UI (verification flow, AI-curated feed, AI-assisted profile creation) across 4 of 5 screenshots to prove its “AI” claim functionally, not just assert it in copy.",
            "Visible reviews contradict the shipped polish implied by the screenshots — slow uploads, multi-day “profile under review” delays, and a broken “finding you matches” screen — a real gap between marketing promise and product worth watching for any app's own ASO-to-QA consistency.",
            "Blends matrimony-style profile fields (caste/community, education, height) into a modern swipe-card UI — a distinctly India-market hybrid pattern not seen in any Western listing reviewed.",
        ],
    ),
]

GROUPS = []
for a in APPS:
    if a["group"] not in GROUPS:
        GROUPS.append(a["group"])

def img(app_slug, filename, alt=""):
    return f'report-images/{app_slug}/{filename}'

def app_section(a):
    rows = "".join(
        f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>"
        for k, v in [
            ("Package", a["package"]), ("Developer", a["developer"]),
            ("Rating", f'{a["rating"]} stars ({a["reviews"]} reviews)'),
            ("Installs", a["installs"]), ("Monetization", a["monetization"]),
            ("Content rating", a["content_rating"]), ("Category badge", a["badge"]),
            ("Last updated", a["updated"]),
        ]
    )
    shots_html = "".join(
        f'<figure class="shot"><img src="{img(a["slug"], fn)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>'
        for fn, cap in a["shots"]
    )
    aso_html = "".join(f"<li>{esc(b)}</li>" for b in a["aso"])
    return f'''
<section class="app-profile" id="{a["slug"]}">
  <div class="app-header">
    <img class="app-icon" src="{img(a["slug"], "icon.jpg")}">
    <div>
      <h3>{esc(a["name"])}</h3>
      <p class="short-desc">&ldquo;{esc(a["short_desc"])}&rdquo;</p>
    </div>
  </div>
  <table class="meta-table">{rows}</table>
  <h4>Description &amp; positioning</h4>
  <p>{esc(a["summary"])}</p>
  <p class="whats-new"><strong>What's new:</strong> {esc(a["whats_new"])}</p>
  <h4>Screenshot carousel</h4>
  <div class="shot-grid">{shots_html}</div>
  <h4>Notable ASO / attractiveness tactics</h4>
  <ul>{aso_html}</ul>
</section>
'''

comparison_rows = "".join(
    f'''<tr>
        <td>{esc(a["name"].split(" - ")[0].split(":")[0].split("—")[0].strip())}</td>
        <td>{esc(a["rating"])}★</td>
        <td>{esc(a["installs"])}</td>
        <td>{esc(a["badge"])}</td>
        <td>{esc(a["group"])}</td>
    </tr>''' for a in APPS
)

toc_items = "".join(f'<li><a href="#{a["slug"]}">{esc(a["name"])}</a></li>' for a in APPS)

HTML = f'''<!doctype html>
<html><head><meta charset="utf-8">
<title>Riteangle Competitive Play Store Audit</title>
<style>
  @page {{ size: A4; margin: 20mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: "Helvetica Neue", Arial, sans-serif; color: #1c1c1e; line-height: 1.5; font-size: 10.5pt; }}
  h1 {{ font-size: 26pt; margin-bottom: 4px; }}
  h2 {{ font-size: 17pt; margin-top: 36px; border-bottom: 3px solid #d1006b; padding-bottom: 6px; page-break-before: always; }}
  h2.no-break {{ page-break-before: auto; }}
  h3 {{ font-size: 14pt; margin: 0; }}
  h4 {{ font-size: 11pt; color: #d1006b; margin-top: 16px; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.04em; }}
  .cover {{ text-align: center; padding-top: 22vh; }}
  .cover h1 {{ font-size: 32pt; }}
  .cover .sub {{ font-size: 13pt; color: #555; margin-top: 8px; }}
  .cover .meta {{ margin-top: 60px; font-size: 10pt; color: #777; }}
  .badge-row {{ display:flex; gap: 8px; justify-content: center; margin-top: 24px; flex-wrap: wrap; }}
  .badge {{ background:#f4e6ee; color:#a3005a; padding: 4px 10px; border-radius: 12px; font-size: 9pt; }}
  section.app-profile {{ page-break-before: always; padding-top: 4px; }}
  .app-header {{ display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }}
  .app-icon {{ width: 64px; height: 64px; border-radius: 14px; object-fit: cover; flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,.25); }}
  .short-desc {{ color: #555; font-style: italic; margin: 2px 0 0; }}
  table.meta-table {{ border-collapse: collapse; width: 100%; margin: 8px 0 4px; font-size: 9.5pt; }}
  table.meta-table th {{ text-align: left; background: #faf1f6; padding: 4px 8px; width: 130px; border: 1px solid #eee; color: #6b0035; }}
  table.meta-table td {{ padding: 4px 8px; border: 1px solid #eee; }}
  .whats-new {{ font-size: 9.5pt; color: #444; background: #f7f7f7; padding: 6px 10px; border-left: 3px solid #d1006b; }}
  .shot-grid {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 6px; }}
  figure.shot {{ width: 18.5%; margin: 0; }}
  figure.shot img {{ width: 100%; border-radius: 8px; border: 1px solid #ddd; display:block; }}
  figure.shot figcaption {{ font-size: 7.6pt; color: #555; margin-top: 3px; line-height: 1.3; }}
  ul {{ margin: 4px 0; padding-left: 20px; }}
  li {{ margin-bottom: 4px; }}
  table.compare {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; margin-top: 10px; }}
  table.compare th, table.compare td {{ border: 1px solid #ddd; padding: 6px 8px; text-align: left; }}
  table.compare th {{ background: #faf1f6; color: #6b0035; }}
  .group-tag {{ display:inline-block; background:#eee; border-radius: 10px; padding: 1px 8px; font-size: 8.5pt; color:#555; }}
  .toc {{ columns: 2; column-gap: 30px; font-size: 9.5pt; }}
  .toc li {{ margin-bottom: 3px; }}
  .callout {{ background: #fff6fa; border: 1px solid #f2c9de; border-radius: 8px; padding: 14px 18px; margin: 12px 0; }}
  .two-col {{ display:flex; gap: 24px; }}
  .two-col > div {{ flex: 1; }}
  footer.pagefoot {{ font-size: 8pt; color:#999; text-align:center; margin-top: 40px; }}
</style>
</head>
<body>

<div class="cover">
  <h1>Riteangle Competitive<br>Play Store Audit</h1>
  <div class="sub">A baseline study of 14 dating &amp; matrimony apps' Android store listings<br>(Google Play, India store, English) &mdash; screenshots, descriptions, and ASO tactics</div>
  <div class="badge-row">
    <span class="badge">14 apps audited</span>
    <span class="badge">84 screenshots captured</span>
    <span class="badge">Global swipe apps</span>
    <span class="badge">India-focused dating</span>
    <span class="badge">India matrimony</span>
  </div>
  <div class="meta">Prepared for Riteangle &middot; September 2, 2026 &middot; Internal / competitive-intelligence use only &mdash; not for redistribution</div>
</div>

<h2 class="no-break" style="page-break-before: always;">Contents</h2>
<ul class="toc">{toc_items}</ul>

<h2>Executive Summary</h2>
<p>This report is the baseline step in a three-part project: (1) understand how competing dating and
matrimony apps present themselves on the Google Play Store today, (2) infer what Riteangle's own
listing should say and show, and (3) develop the creatives and update the live listing. Only step
(1) is covered here.</p>
<p>Fourteen apps were audited directly on the Google Play Store (India storefront, English), split
across three groups: global mainstream swipe apps (Tinder, Bumble, Hinge, happn, OkCupid, Badoo,
Coffee Meets Bagel), India-focused modern dating apps (Aisle, QuackQuack, FRND), and India matrimony
/ marriage-intent apps (Shaadi.com, BharatMatrimony, Betterhalf, Knot). A fifteenth planned entrant,
<strong>Woo</strong> (the India-founded dating app formerly by U2opia Mobile), could not be located on
the current Play Store &mdash; its listing appears to have been delisted or repositioned to a US 30+
market under a different name (see the note at the end of this report). Nothing was substituted in
its place.</p>
<p>Three cross-cutting findings stand out. First, <strong>screenshot strategy splits cleanly into three
templates</strong>: pure lifestyle/emotion photography with no UI (Tinder, Shaadi.com's opening slides,
Betterhalf's entire carousel), literal device-framed in-app UI proof (BharatMatrimony, QuackQuack,
OkCupid, Knot), and a hybrid that opens with one or two emotional hero shots before pivoting to real UI
(Bumble, Hinge, Aisle, Coffee Meets Bagel, Badoo, happn, FRND) &mdash; the hybrid pattern is the most
common and arguably the safest default. Second, <strong>India-market trust deficit is the dominant theme
in copy, not romance</strong>: verification badges (selfie, phone, ID, Aadhaar-adjacent), fake-profile
callouts, and "genuine profiles" language appear in nearly every India-relevant listing (QuackQuack,
Shaadi.com, BharatMatrimony, Betterhalf, Aisle, Knot), because it is the specific objection India users
raise in reviews. Third, <strong>a single negative-review pattern recurs across almost every paid app in
the set regardless of category or rating</strong> &mdash; users report that matches or profile visibility
"dry up" immediately after they pay for a subscription. This shows up in Tinder, Aisle, Shaadi.com,
BharatMatrimony, and OkCupid's own review threads, independent of how polished the listing is. That
consistency is a real whitespace opportunity for a differentiated trust/monetization narrative, not
just a listing-design one.</p>

<h2>Comparison at a Glance</h2>
<table class="compare">
  <tr><th>App</th><th>Rating</th><th>Installs</th><th>Category badge</th><th>Segment</th></tr>
  {comparison_rows}
</table>

<h2>Anatomy of an Attractive Play Store Listing</h2>
<p>Pulling from all 14 audits, these are the recurring, nameable components that make a listing land
&mdash; and the ones that visibly don't.</p>

<h4>1. Title &amp; short description</h4>
<ul>
  <li><strong>Verb-stacked titles win search intent.</strong> Tinder ("Match. Chat. Date."), Bumble ("Dating
  App &amp; Friends"), and QuackQuack ("Dating App in India") all pack the exact phrases a user types into
  search directly into the title, rather than relying on brand name alone.</li>
  <li><strong>Brand-only titles (Shaadi.com, Betterhalf) push all keyword work into the description</strong>
  instead &mdash; a valid alternative once brand recognition is already high, but it means a new or
  smaller app (like Knot, at 598 reviews) needs the title to do more of the work.</li>
  <li><strong>The short description is the only copy guaranteed to be read</strong> &mdash; it's the one line
  shown in search results before a tap. The strongest examples state a differentiator in under 12 words
  (Hinge: "designed to be deleted"; Aisle: "Built for real commitment"; CMB: "for serious daters") rather
  than a generic feature list.</li>
</ul>

<h4>2. Icon &amp; screenshot visual system</h4>
<ul>
  <li><strong>One consistent color field, repeated on every screenshot and the icon</strong>, is the single
  most reliable "looks professional" signal &mdash; Bumble's yellow/black, Aisle's magenta, QuackQuack's
  mustard, happn's near-black-then-cream duo, Knot's maroon. Betterhalf and Shaadi.com's red/magenta systems
  work the same way even though their screenshots are illustrated rather than photographed.</li>
  <li><strong>The hybrid screenshot order (emotion first, proof second) is the dominant winning pattern.</strong>
  Bumble, Hinge, Aisle, Coffee Meets Bagel, Badoo, happn, and FRND all open with one or two lifestyle/brand
  photos before shifting to literal device-framed UI for the remaining 3&ndash;4 slides. This sells the
  outcome before proving the mechanism.</li>
  <li><strong>Real device-frame chrome (bezel, notch, status bar) reads as more "authentic app," borderless
  marketing cards read as more "produced brand."</strong> Aisle and BharatMatrimony use real bezels; Betterhalf
  uses none at all across any of its five screenshots &mdash; a prospective installer literally cannot see the
  product before installing, which is a self-imposed transparency gap none of the higher-rated apps share.</li>
  <li><strong>Baking a stat directly into the first screenshot</strong> (Aisle's "4.5 Rating &middot; 20M+
  Members &middot; 9K Matches/day" row; QuackQuack's "40 Million Users" strap line) makes the value
  proposition scannable in the one frame most likely to appear as a search-result thumbnail.</li>
</ul>

<h4>3. Description structure &amp; tone</h4>
<ul>
  <li><strong>Emoji density is a deliberate tone choice, not filler</strong> &mdash; it ranges from zero
  (Hinge, happn, OkCupid, Betterhalf, Aisle, Knot, BharatMatrimony) to extremely high (Tinder, Bumble, FRND).
  Zero-emoji listings read as premium/editorial; high-emoji listings read as playful/scannable. Neither is
  wrong, but it should match the brand voice deliberately rather than defaulting to "some emoji because
  competitors have them."</li>
  <li><strong>Social proof comes in three flavors, and the strongest listings stack more than one</strong>:
  raw numbers (Tinder's 60B matches, Shaadi.com's 35M members, Betterhalf's 20 lakh profiles), third-party
  press quotes (Hinge and Coffee Meets Bagel both quote named outlets), and Google-granted badges (rank
  positions, Editors' Choice). CMB stacks all three at once.</li>
  <li><strong>Named, specific paid tiers build more trust than vague "premium" language.</strong> Bumble,
  Hinge, Aisle, and Badoo all name their subscription products and, in Aisle's and Hinge's case, disclose
  auto-renewal terms plainly &mdash; versus Betterhalf, Knot, OkCupid, and Coffee Meets Bagel, which describe
  perks without ever naming a price or renewal term.</li>
  <li><strong>Keyword-stacking for India-specific long-tail search is near-universal among India-relevant
  apps</strong> &mdash; religions, castes/communities, regional languages, and cities are enumerated
  explicitly in Shaadi.com, BharatMatrimony, Betterhalf, and (for cities) QuackQuack. BharatMatrimony's
  bilingual English+Hindi opening block is the single most India-localized text treatment in the set.</li>
</ul>

<h4>4. Trust &amp; safety signaling</h4>
<ul>
  <li><strong>Verification badges shown literally inside a screenshot</strong> (Selfie Verified, ID Verified,
  Photo Verified) beat verification merely claimed in prose &mdash; Coffee Meets Bagel, BharatMatrimony, Aisle,
  and Shaadi.com all put a real badge graphic directly on a profile card screenshot.</li>
  <li><strong>A category rank badge or an Editors' Choice mark is free, Google-granted credibility</strong>
  that several apps in this set (Betterhalf, BharatMatrimony, Shaadi.com, Aisle, OkCupid, Knot, Badoo)
  simply don't have &mdash; worth checking eligibility for, since it costs nothing to display once earned.</li>
  <li><strong>Personalized developer replies to negative reviews</strong> (Shaadi.com uses the reviewer's
  first name; BharatMatrimony's replies are more templated) is a visible, low-cost reputation-management
  signal that shows up directly on the listing page itself, where any visitor can see it before installing.</li>
</ul>

<h4>5. Monetization transparency</h4>
<p>Listings sit on a clear spectrum from fully disclosed to fully opaque:</p>
<div class="callout">
  <strong>Most transparent</strong> &mdash; Aisle, Hinge, Bumble, Badoo (name every paid tier, disclose
  auto-renewal terms in the description itself, and in Badoo's case even show a literal pay-per-message
  coin cost inside a screenshot).<br><br>
  <strong>Perks-described-but-unpriced</strong> &mdash; Coffee Meets Bagel, OkCupid, Betterhalf, QuackQuack
  (name the premium tier and list its benefits, but no price or renewal terms appear in the visible copy).<br><br>
  <strong>Fully opaque</strong> &mdash; Knot (no ads/IAP badge, no pricing language anywhere; consistent
  with its invite-only positioning).
</div>

<h2>Recurring Weaknesses &amp; Whitespace</h2>
<p>These patterns showed up in the sampled user reviews across multiple, otherwise-unrelated apps &mdash;
worth treating as category-level pain points rather than one app's problem:</p>
<ul>
  <li><strong>"Matches dry up right after I paid" is the single most repeated complaint</strong>, appearing
  in review samples for Tinder, Aisle, Shaadi.com, BharatMatrimony, and OkCupid alike. A listing (and
  product) that can credibly promise the opposite &mdash; continuity or a replacement guarantee &mdash; is
  addressing a documented, cross-category trust gap, not inventing a claim.</li>
  <li><strong>Fake or bot-like profiles</strong> are called out by name in Shaadi.com and BharatMatrimony
  reviews specifically, despite both apps' heavy verification messaging &mdash; suggesting the badges alone
  aren't fully closing the credibility gap for skeptical users.</li>
  <li><strong>Forced sign-in and account-lockout friction</strong> (happn's forced Google Sign-In complaints;
  Tinder's photo-verification lockouts; FRND's arbitrary-ban complaints) show up as a secondary but real
  reputation risk sitting underneath otherwise-strong star ratings.</li>
  <li><strong>Illustrated-only screenshots (Betterhalf) mean zero real-product visibility before install</strong>
  &mdash; a self-imposed transparency gap that no other app in this set shares, and one worth avoiding
  deliberately rather than by accident.</li>
</ul>

<h2>Individual Competitor Profiles</h2>
<p>The following pages cover each of the 14 audited apps in the order shown in the comparison table, grouped
by segment: global mainstream swipe apps, India-focused modern dating apps, and India matrimony /
marriage-intent apps.</p>

{"".join(app_section(a) for a in APPS)}

<h2>Note: Woo (could not be completed)</h2>
<p>Woo &mdash; the India-founded dating app historically operated by U2opia Mobile under the package id
<code>com.u2opia.woo</code> &mdash; could not be located on the Google Play India store as of this audit.
Direct package-id lookups returned "Not Found," and web search suggests the listing may have been
repositioned toward a US 30+ dating market under a different title, or delisted outright. A separately
named app, "WooPlus" (curvy/body-positive dating, a different market and positioning), and an unrelated
US micro-app also called "Woo Dating" were both checked and correctly excluded as non-matches. No
screenshots or notes were substituted in Woo's place. <strong>Recommendation:</strong> confirm whether Woo
should be dropped from the competitive set going forward, or replaced with an active alternative &mdash;
"you&amp;me" and IndianCupid surfaced repeatedly as adjacent India-market alternatives during the search.</p>

<h2>Next Steps</h2>
<p>This report closes the baseline-research phase. The next two steps, per the original brief, are: (1)
use the patterns above to infer what Riteangle's own Play Store listing should say and show, and (2)
develop the actual creatives (icon, screenshots, description copy) before updating the live listing.
Both should be treated as separate, deliberate follow-on pieces of work rather than folded into this
audit.</p>

<footer class="pagefoot">Riteangle competitive intelligence &middot; internal use only &middot; compiled 2026-09-02</footer>

</body></html>
'''

os.makedirs(OUT_DIR, exist_ok=True)
report_path = os.path.join(OUT_DIR, "report.html")
with open(report_path, "w") as f:
    f.write(HTML)
print("wrote", report_path, len(HTML), "bytes")
