import json
from database import get_db, init_db

LESSONS = [
    # ── Module 1 · Ages 10–12 ──────────────────────────────────────────────
    {
        "id": "plastic-m1-10-12",
        "title": "The Plastic Story (Ages 10–12)",
        "description": "Discover where plastic comes from and why it became so widespread — tracing its journey from crude oil to everyday objects.",
        "full_description": (
            "Students explore the origins of plastic as a petroleum-derived material, "
            "examining the industrial processes that convert crude oil into the polymers "
            "found in bottles, bags, and packaging. The module introduces chemical bonds, "
            "polymer chains, and why plastic's durability — once its biggest selling point "
            "— is now its biggest environmental problem. Age-appropriate analogies and "
            "hands-on sorting activities ground abstract chemistry in familiar objects."
        ),
        "age_group": "10-12",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic origins", "fossil fuels", "polymer chemistry", "product lifecycle"]),
        "learning_outcomes": json.dumps([
            "Explain that most plastics are derived from fossil fuels",
            "Describe the basic concept of a polymer chain in everyday language",
            "Identify common single-use plastics in the home and name their resin codes",
            "Articulate why plastic's durability creates long-term environmental challenges",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "worksheet", "activity"]),
        "sdg_alignment": json.dumps([4, 12, 13]),
        "language": "en",
        "duration_per_module_minutes": 25,
        "duration_total_minutes": 125,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-story-10-12",
        "is_free": 1,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Plastic Origins Map — students trace a plastic bottle back to an oil field",
            "Polymer Puzzle — label and sort polymer-chain diagrams",
        ]),
        "discussion_prompts": json.dumps([
            "If plastic is so durable, why don't we reuse it more instead of throwing it away?",
            "Who decided plastic should be single-use? Was that a good idea at the time?",
        ]),
    },

    # ── Module 1 · Ages 13–16 ──────────────────────────────────────────────
    {
        "id": "plastic-m1-13-16",
        "title": "The Plastic Story (Ages 13–16)",
        "description": "Trace plastic from petrochemical feedstock to global commodity — and examine the economic and political forces that shaped its rise.",
        "full_description": (
            "This module situates plastic within the broader history of the petrochemical "
            "industry, examining how lobbying, marketing, and infrastructure lock-in "
            "entrenched single-use culture. Students analyse primary sources — including "
            "Keep America Beautiful campaign materials — and evaluate how producer "
            "responsibility was deliberately shifted onto consumers. The module introduces "
            "life-cycle assessment (LCA) as a tool for comparing environmental costs across "
            "materials, and challenges students to question 'common knowledge' about recycling."
        ),
        "age_group": "13-16",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic origins", "fossil fuels", "producer responsibility", "life-cycle assessment", "political economy"]),
        "learning_outcomes": json.dumps([
            "Analyse the historical role of the petrochemical industry in promoting single-use plastic",
            "Explain life-cycle assessment and apply it to compare two packaging materials",
            "Critically evaluate how corporate campaigns shifted environmental responsibility to consumers",
            "Identify structural barriers to reducing plastic production",
        ]),
        "pedagogical_approach": "critical inquiry",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 12, 13]),
        "language": "en",
        "duration_per_module_minutes": 30,
        "duration_total_minutes": 150,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-story-13-16",
        "is_free": 1,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "LCA Comparison Sheet — compare PET bottle vs glass bottle across five lifecycle stages",
            "Source Analysis: Keep America Beautiful — annotate a historical ad and identify rhetorical strategies",
        ]),
        "discussion_prompts": json.dumps([
            "Should plastic producers — not consumers — be legally responsible for end-of-life costs?",
            "Is it possible to separate plastic as a material from the fossil fuel industry? Why or why not?",
        ]),
    },

    # ── Module 2 · Ages 10–12 ──────────────────────────────────────────────
    {
        "id": "plastic-m2-10-12",
        "title": "Plastic Types & Recyclability (Ages 10–12)",
        "description": "Learn why the recycling triangle on plastic doesn't mean it will actually be recycled — and what the numbers really mean.",
        "full_description": (
            "Students examine the seven resin identification codes and discover that most "
            "plastic types are technically recyclable but economically or logistically "
            "unrecyclable in practice. The module uses sorting simulations to reveal how "
            "contamination, market demand, and infrastructure gaps determine what actually "
            "gets processed. Students come away understanding that the recycling symbol is "
            "a material identifier, not a guarantee of recycling."
        ),
        "age_group": "10-12",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic types", "recycling systems", "resin codes", "contamination"]),
        "learning_outcomes": json.dumps([
            "Identify the seven resin codes and name one common product for each",
            "Distinguish between 'technically recyclable' and 'practically recycled'",
            "Explain how contamination reduces the value of recyclable material",
            "Describe why market demand affects which plastics get recycled",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "worksheet", "activity"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 25,
        "duration_total_minutes": 125,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-types-10-12",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Resin Code Spotter — find and record 10 items at home with their resin codes",
            "Recyclable vs Recycled — sort 20 plastic items into three categories",
        ]),
        "discussion_prompts": json.dumps([
            "If a plastic has a recycling triangle on it but your council won't collect it, is it actually recyclable?",
            "Who should decide what counts as 'recyclable' — the manufacturer or the recycler?",
        ]),
    },

    # ── Module 2 · Ages 13–16 ──────────────────────────────────────────────
    {
        "id": "plastic-m2-13-16",
        "title": "Plastic Types & Recyclability (Ages 13–16)",
        "description": "Interrogate the gap between recycling claims and recycling reality — examining commodity markets, contamination economics, and greenwashing.",
        "full_description": (
            "Students conduct a deep dive into why the global recyclability rate for plastic "
            "sits below 10%, despite decades of public education campaigns. The module covers "
            "polymer chemistry differences between resin types, the economics of secondary "
            "materials markets, and how brand labelling practices contribute to consumer "
            "confusion. Students evaluate recent extended producer responsibility (EPR) "
            "legislation in the EU and California and assess whether regulation or market "
            "forces are more likely to close the recyclability gap."
        ),
        "age_group": "13-16",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic types", "recycling systems", "producer responsibility", "greenwashing", "circular economy"]),
        "learning_outcomes": json.dumps([
            "Explain why global plastic recycling rates remain below 10% despite widespread collection infrastructure",
            "Evaluate the role of secondary materials markets in determining recyclability outcomes",
            "Analyse a product label and identify potential greenwashing claims",
            "Compare EPR legislation in two jurisdictions and assess likely effectiveness",
        ]),
        "pedagogical_approach": "real-world trade-offs",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 30,
        "duration_total_minutes": 150,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-types-13-16",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Market Price Tracker — research current commodity prices for PET, HDPE, and mixed plastics",
            "Greenwash Audit — analyse three brand sustainability claims against third-party data",
        ]),
        "discussion_prompts": json.dumps([
            "Should it be illegal to label packaging as 'recyclable' if local infrastructure can't process it?",
            "Is voluntary industry action ever sufficient to close a systemic gap, or does regulation always need to lead?",
        ]),
    },

    # ── Module 3 · Ages 10–12 ──────────────────────────────────────────────
    {
        "id": "plastic-m3-10-12",
        "title": "Waste Systems & Infrastructure (Ages 10–12)",
        "description": "Follow your rubbish bin after collection — mapping the sorting facilities, trucks, and workers that make (or break) local recycling.",
        "full_description": (
            "Students map the waste journey from kerbside bin to materials recovery facility "
            "(MRF), landfill, or export. The module uses visual system diagrams to show how "
            "collection frequency, sorting technology, and local government contracts shape "
            "what actually happens to waste. Students discover that recycling outcomes vary "
            "dramatically by postcode — even within the same country — and begin to understand "
            "waste as an infrastructure and governance challenge, not just a behaviour one."
        ),
        "age_group": "10-12",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["recycling systems", "waste infrastructure", "MRF", "local government", "waste trade"]),
        "learning_outcomes": json.dumps([
            "Trace the journey of a plastic bottle from kerbside bin to end destination",
            "Explain what a materials recovery facility does and how sorting works",
            "Describe why recycling outcomes differ between local areas",
            "Identify at least two ways infrastructure affects individual recycling behaviour",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "worksheet", "activity"]),
        "sdg_alignment": json.dumps([4, 11, 12]),
        "language": "en",
        "duration_per_module_minutes": 25,
        "duration_total_minutes": 125,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/waste-systems-10-12",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Waste Journey Map — draw the route from your bin to each possible end destination",
            "Postcode Comparison — compare local council recycling rules with a neighbouring area",
        ]),
        "discussion_prompts": json.dumps([
            "If recycling outcomes depend on where you live, is it fair to blame individuals for not recycling properly?",
            "What would you change about your local waste system if you were in charge?",
        ]),
    },

    # ── Module 3 · Ages 13–16 ──────────────────────────────────────────────
    {
        "id": "plastic-m3-13-16",
        "title": "Waste Systems & Infrastructure (Ages 13–16)",
        "description": "Examine how waste policy, contract structures, and the global waste trade determine what actually gets recycled — and who bears the cost.",
        "full_description": (
            "This module analyses waste management as a policy and infrastructure system, "
            "examining procurement models (in-house vs private contractor), gate fees, "
            "landfill taxes, and how MRF technology investment decisions are made. Students "
            "study the 2018 China National Sword policy and its cascading effects on recycling "
            "systems worldwide. The module also explores waste colonialism — the practice of "
            "exporting waste to lower-income countries — and evaluates the Basel Convention "
            "plastic waste amendments as a regulatory response."
        ),
        "age_group": "13-16",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["recycling systems", "waste infrastructure", "waste trade", "waste colonialism", "policy"]),
        "learning_outcomes": json.dumps([
            "Analyse the impacts of China's National Sword policy on global recycling infrastructure",
            "Explain the concept of waste colonialism and identify examples in the global waste trade",
            "Evaluate the Basel Convention plastic waste amendments and their enforcement challenges",
            "Assess the trade-offs between privatised and municipal waste management models",
        ]),
        "pedagogical_approach": "real-world trade-offs",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 10, 11, 12, 17]),
        "language": "en",
        "duration_per_module_minutes": 30,
        "duration_total_minutes": 150,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/waste-systems-13-16",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "National Sword Case Study — map the policy change and its documented downstream effects",
            "Basel Convention Analysis — evaluate the 2019 plastic waste amendments for three signatory countries",
        ]),
        "discussion_prompts": json.dumps([
            "Is it ethical for wealthy countries to export plastic waste to countries with weaker environmental regulations?",
            "Should waste management be a public service or a private market? What are the trade-offs?",
        ]),
    },

    # ── Module 4 · Ages 10–12 ──────────────────────────────────────────────
    {
        "id": "plastic-m4-10-12",
        "title": "Ocean Plastic & Ecosystems (Ages 10–12)",
        "description": "Explore how plastic enters waterways, forms ocean gyres, breaks into microplastics, and disrupts marine food webs.",
        "full_description": (
            "Students follow plastic from land sources through river systems to the ocean, "
            "learning how gyres concentrate debris into 'garbage patches'. The module covers "
            "photodegradation and the formation of microplastics, and uses food web diagrams "
            "to show how plastic moves through marine ecosystems — from plankton to fish to "
            "seabirds. Students also explore the human dimension: coastal fishing communities "
            "whose livelihoods depend on healthy oceans. The module avoids catastrophism in "
            "favour of building accurate mental models of how pollution spreads through systems."
        ),
        "age_group": "10-12",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["ocean plastic", "microplastics", "marine ecosystems", "food webs", "pollution pathways"]),
        "learning_outcomes": json.dumps([
            "Trace the pathway of plastic from land sources to ocean gyres",
            "Explain what microplastics are and how they form",
            "Describe how microplastics move through a marine food web",
            "Identify communities whose livelihoods are most affected by ocean plastic",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "worksheet", "activity"]),
        "sdg_alignment": json.dumps([4, 13, 14]),
        "language": "en",
        "duration_per_module_minutes": 25,
        "duration_total_minutes": 125,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/ocean-plastic-10-12",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Ocean Gyre Map — mark the five major gyres and identify the largest debris concentrations",
            "Food Web Diagram — trace microplastic transfer across five trophic levels",
        ]),
        "discussion_prompts": json.dumps([
            "If plastic breaks into smaller pieces but doesn't disappear, where does it actually go?",
            "Should people who live far from the ocean worry about ocean plastic? Why?",
        ]),
    },

    # ── Module 4 · Ages 13–16 ──────────────────────────────────────────────
    {
        "id": "plastic-m4-13-16",
        "title": "Ocean Plastic & Ecosystems (Ages 13–16)",
        "description": "Assess the scientific evidence on ocean plastic impacts — and evaluate cleanup technology, community solutions, and the limits of both.",
        "full_description": (
            "Students review peer-reviewed research on microplastic bioaccumulation, "
            "chemical leaching, and impacts on marine biodiversity. The module critically "
            "examines high-profile ocean cleanup technologies — including The Ocean Cleanup "
            "project — evaluating evidence for effectiveness and unintended consequences "
            "such as bycatch. Students also analyse community-led source-reduction programmes "
            "in the Philippines and Indonesia and assess why downstream solutions are "
            "structurally limited compared to upstream prevention."
        ),
        "age_group": "13-16",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["ocean plastic", "microplastics", "marine ecosystems", "cleanup technology", "source reduction"]),
        "learning_outcomes": json.dumps([
            "Summarise the scientific evidence on microplastic bioaccumulation and human health implications",
            "Critically evaluate the evidence base for ocean cleanup technology effectiveness",
            "Compare upstream source reduction with downstream cleanup as policy responses",
            "Analyse a community-led plastic reduction programme and assess its transferability",
        ]),
        "pedagogical_approach": "critical inquiry",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 13, 14]),
        "language": "en",
        "duration_per_module_minutes": 30,
        "duration_total_minutes": 150,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/ocean-plastic-13-16",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Technology Evaluation Matrix — score three ocean cleanup technologies across five criteria",
            "Community Case Study: Philippines — analyse a fishing village programme using a systems lens",
        ]),
        "discussion_prompts": json.dumps([
            "Is investing in ocean cleanup technology a distraction from addressing plastic production? Defend your view.",
            "Who should fund ocean cleanup — governments, corporations, or individuals? On what basis?",
        ]),
    },

    # ── Module 5 · Ages 10–12 ──────────────────────────────────────────────
    {
        "id": "plastic-m5-10-12",
        "title": "Circular Economy & Trade-offs (Ages 10–12)",
        "description": "Discover what a circular economy really means — and why turning 'good ideas' into working systems is harder than it sounds.",
        "full_description": (
            "Students are introduced to the circular economy concept through the 'reduce, "
            "reuse, recycle' hierarchy, and then examine real examples to see where the model "
            "works and where it breaks down. Case studies include refillable packaging pilots, "
            "deposit return schemes, and product-as-a-service models. Students complete a "
            "trade-off activity that shows how solutions that work at small scale can create "
            "new problems at large scale — building honest intuitions about systemic change."
        ),
        "age_group": "10-12",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["circular economy", "waste hierarchy", "deposit return schemes", "systems thinking", "trade-offs"]),
        "learning_outcomes": json.dumps([
            "Explain the circular economy concept and how it differs from linear 'take-make-dispose'",
            "Apply the waste hierarchy to rank responses to a specific plastic problem",
            "Describe at least two real-world circular economy interventions and how they work",
            "Identify one trade-off or unintended consequence in a proposed solution",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "worksheet", "activity", "reflection"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 25,
        "duration_total_minutes": 125,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/circular-economy-10-12",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Waste Hierarchy Ranking — apply the hierarchy to five everyday plastic scenarios",
            "Scale-Up Challenge — identify what breaks when a small circular pilot goes national",
        ]),
        "discussion_prompts": json.dumps([
            "Is recycling the best solution to plastic waste, or just the easiest to sell?",
            "Can a circular economy work if companies still need to grow every year?",
        ]),
    },

    # ── Module 5 · Ages 13–16 ──────────────────────────────────────────────
    {
        "id": "plastic-m5-13-16",
        "title": "Circular Economy & Trade-offs (Ages 13–16)",
        "description": "Stress-test circular economy proposals against real-world constraints — from energy costs to global supply chains to political economy.",
        "full_description": (
            "Students critically analyse circular economy frameworks (Ellen MacArthur "
            "Foundation model, EU Circular Economy Action Plan) and evaluate whether "
            "they represent a genuine systems shift or incremental improvement within "
            "existing growth models. The module examines the rebound effect, the "
            "energy costs of recycling, and the role of international trade rules in "
            "constraining national circular economy policy. Students design a policy "
            "proposal for one plastic sub-sector (food packaging, textiles, electronics) "
            "and stress-test it against stakeholder interests and systemic constraints."
        ),
        "age_group": "13-16",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["circular economy", "producer responsibility", "rebound effect", "policy design", "trade-offs", "systems thinking"]),
        "learning_outcomes": json.dumps([
            "Critically evaluate circular economy frameworks against alternative economic models",
            "Explain the rebound effect and apply it to a circular economy case study",
            "Design a policy intervention for one plastic sub-sector and identify key trade-offs",
            "Assess how international trade rules constrain national circular economy ambition",
        ]),
        "pedagogical_approach": "real-world trade-offs",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection", "activity"]),
        "sdg_alignment": json.dumps([4, 8, 12, 13, 17]),
        "language": "en",
        "duration_per_module_minutes": 30,
        "duration_total_minutes": 150,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/circular-economy-13-16",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Framework Comparison — map Ellen MacArthur Foundation and EU CEAP against a degrowth critique",
            "Policy Design Studio — draft a plastic sub-sector intervention and complete a stakeholder impact grid",
        ]),
        "discussion_prompts": json.dumps([
            "Can a circular economy exist within a system that requires continuous economic growth? What would have to change?",
            "Who benefits most from circular economy narratives — corporations, governments, or citizens?",
        ]),
    },
]

LESSONS_6_9 = [
    # ── Module 1 · Ages 6–9 ───────────────────────────────────────────────
    {
        "id": "plastic-m1-6-9",
        "title": "The Plastic Story (Ages 6–9)",
        "description": "Meet plastic! Find out where it comes from, why grown-ups started making so much of it, and why that turned out to be a really tricky problem.",
        "full_description": (
            "Told through narrated animation and guided storytime, this module introduces "
            "young learners to plastic as a made-up material — something humans invented from "
            "oil found deep underground. Children explore their own homes to find plastic "
            "objects and begin to notice just how many there are. A simple 'plastic parade' "
            "activity builds vocabulary and curiosity without introducing anxiety. The module "
            "ends with the key question: if plastic lasts forever, where does it go when we "
            "throw it away?"
        ),
        "age_group": "6-9",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic origins", "everyday plastic", "materials", "curiosity"]),
        "learning_outcomes": json.dumps([
            "Name plastic as a human-made material that comes from oil",
            "Find and count plastic objects in their everyday environment",
            "Explain in simple terms why plastic lasting a long time can be a problem",
            "Ask a question about what happens to plastic after we throw it away",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "activity", "reflection"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 15,
        "duration_total_minutes": 75,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-story-6-9",
        "is_free": 1,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Plastic Parade — draw or list 10 plastic things you can find at home",
            "Where Did It Come From? — match pictures of plastic objects to pictures of oil wells and factories",
        ]),
        "discussion_prompts": json.dumps([
            "If you had to live without plastic for one day, what would be the hardest thing to give up?",
            "Why do you think people started making so much plastic?",
        ]),
    },

    # ── Module 2 · Ages 6–9 ───────────────────────────────────────────────
    {
        "id": "plastic-m2-6-9",
        "title": "Not All Plastic Is the Same (Ages 6–9)",
        "description": "Did you know there are seven different kinds of plastic — and most of them can't be recycled where you live? Let's find out why.",
        "full_description": (
            "Using colour-coded sorting cards, children learn that the little number inside "
            "the recycling triangle tells us what type of plastic something is — not whether "
            "it will actually be recycled. Through a hands-on sorting game, students discover "
            "that most plastic types need special machines that many towns don't have. The "
            "module uses straightforward language to introduce the idea that 'recyclable' "
            "and 'recycled' are different things — a foundational concept for later modules."
        ),
        "age_group": "6-9",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic types", "resin codes", "recycling symbols", "sorting"]),
        "learning_outcomes": json.dumps([
            "Recognise the recycling triangle symbol and explain that the number inside shows the plastic type",
            "Sort common plastic items by resin code using colour-coded cards",
            "State that most plastic types are not recycled in most places",
            "Distinguish between 'recyclable' (could be) and 'recycled' (actually is)",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "activity", "worksheet"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 15,
        "duration_total_minutes": 75,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-types-6-9",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "The Seven Plastics — colour in each type and write one thing made from it",
            "Sorted! — cut out the plastic card images and sort them into 'collected near me' and 'not collected near me'",
        ]),
        "discussion_prompts": json.dumps([
            "If the recycling symbol doesn't mean it gets recycled, why do you think it's still on the packaging?",
            "What would happen if everyone put the wrong plastic in the recycling bin?",
        ]),
    },

    # ── Module 3 · Ages 6–9 ───────────────────────────────────────────────
    {
        "id": "plastic-m3-6-9",
        "title": "Where Does Rubbish Go? (Ages 6–9)",
        "description": "Follow your bin bag on its big journey — from your house, to the truck, to the sorting centre, and beyond.",
        "full_description": (
            "A narrated animated journey follows 'Bag the Bin Bag' from kerbside collection "
            "through a sorting facility and on to its final destination — which might be a "
            "recycling plant, a landfill, or an incinerator. Children map the journey on a "
            "simple flow diagram and discover that what happens to their rubbish depends on "
            "where they live, not just what they put in the bin. The module builds foundational "
            "understanding of waste as an infrastructure system — something that involves "
            "trucks, workers, buildings, and decisions, not just bins."
        ),
        "age_group": "6-9",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["waste infrastructure", "recycling systems", "waste journey", "local government"]),
        "learning_outcomes": json.dumps([
            "Describe at least three steps in the journey from a bin to a waste facility",
            "Name the three main destinations for rubbish: recycling plant, landfill, incinerator",
            "Explain that where you live affects what gets recycled",
            "Identify at least two people whose jobs involve waste",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "activity", "worksheet"]),
        "sdg_alignment": json.dumps([4, 11, 12]),
        "language": "en",
        "duration_per_module_minutes": 15,
        "duration_total_minutes": 75,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/waste-systems-6-9",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Rubbish Journey Map — draw and label the stages from bin to final destination",
            "Waste Workers — draw or write about three jobs that deal with our rubbish",
        ]),
        "discussion_prompts": json.dumps([
            "Who is responsible for making sure rubbish goes to the right place — you, your family, or the council?",
            "What do you think happens to plastic in a landfill after 100 years?",
        ]),
    },

    # ── Module 4 · Ages 6–9 ───────────────────────────────────────────────
    {
        "id": "plastic-m4-6-9",
        "title": "Plastic in the Ocean (Ages 6–9)",
        "description": "Explore how plastic ends up in the sea, what it does to animals and fish, and why people all over the world are trying to stop it.",
        "full_description": (
            "Using illustrated storybook narration and simple diagrams, children follow a "
            "plastic bag from a street drain to a river and into the ocean. The module "
            "introduces ocean gyres using a 'spinning soup bowl' analogy, and explains "
            "microplastics through the image of plastic 'crumbling like a biscuit' in "
            "sunlight. A focus on seabirds and sea turtles makes the impact concrete and "
            "emotionally resonant without being distressing. The module ends with examples "
            "of real children and communities taking action to reduce plastic reaching the sea."
        ),
        "age_group": "6-9",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["ocean plastic", "microplastics", "marine animals", "pollution pathways"]),
        "learning_outcomes": json.dumps([
            "Trace a simple path from a plastic item on land to the ocean",
            "Explain what microplastics are using an everyday analogy",
            "Describe one way ocean plastic harms a marine animal",
            "Name one action a community has taken to reduce plastic reaching the sea",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "activity", "worksheet", "reflection"]),
        "sdg_alignment": json.dumps([4, 13, 14]),
        "language": "en",
        "duration_per_module_minutes": 15,
        "duration_total_minutes": 75,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/ocean-plastic-6-9",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Plastic's Ocean Journey — draw each step as a comic strip from street to sea",
            "Ocean Animal Report — choose one animal and write two sentences about how plastic affects it",
        ]),
        "discussion_prompts": json.dumps([
            "If you live far from the sea, can your plastic still end up in the ocean? How?",
            "What could you do this week to stop one piece of plastic from reaching the sea?",
        ]),
    },

    # ── Module 5 · Ages 6–9 ───────────────────────────────────────────────
    {
        "id": "plastic-m5-6-9",
        "title": "What Can We Do? (Ages 6–9)",
        "description": "Learn about the three Rs — reduce, reuse, recycle — and find out which one is the most powerful. Then make your own plan for using less plastic.",
        "full_description": (
            "This module introduces the waste hierarchy through a simple 'best to least best' "
            "ladder and invites children to evaluate everyday choices against it. Using "
            "relatable examples — water bottles, lunch boxes, carrier bags — students practise "
            "ranking options from 'use less' to 'throw away'. The module is honest that "
            "recycling is not a magic fix, while remaining age-appropriately constructive: "
            "children finish by making a personal 'plastic promise' and designing a poster "
            "for their home or classroom. The emphasis is on individual action as one part "
            "of a bigger system, not the whole solution."
        ),
        "age_group": "6-9",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["waste hierarchy", "reduce reuse recycle", "circular economy", "personal action"]),
        "learning_outcomes": json.dumps([
            "Order 'reduce, reuse, recycle' from most to least effective",
            "Apply the waste hierarchy to at least three everyday plastic choices",
            "Explain in simple terms why recycling alone cannot solve the plastic problem",
            "Make and write down one personal commitment to use less plastic",
        ]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "activity", "worksheet", "reflection"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 15,
        "duration_total_minutes": 75,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/circular-economy-6-9",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "The 3R Ladder — place six everyday scenarios on the right rung of the waste hierarchy",
            "My Plastic Promise — write or draw your personal commitment and decorate it as a poster",
        ]),
        "discussion_prompts": json.dumps([
            "If every person in your class used one less plastic bag a week, how many bags would that save in a year?",
            "Is it enough for just kids to try to use less plastic, or do grown-ups and companies need to change too?",
        ]),
    },
]

LESSONS_17_PLUS = [
    # ── Module 1 · Ages 17+ ───────────────────────────────────────────────
    {
        "id": "plastic-m1-17-plus",
        "title": "The Plastic Story (Ages 17+)",
        "description": "Trace plastic from its petrochemical origins through industrial scale-up and deliberate marketisation — and examine who built this system and why.",
        "full_description": (
            "This module situates plastic within the history of twentieth-century industrial "
            "capitalism, tracing the development of the petrochemical industry from post-WWI "
            "surpluses to the deliberate construction of a throwaway consumer culture. Students "
            "engage with primary sources — including industry documents, advertising archives, "
            "and congressional testimony — and apply political economy frameworks to analyse "
            "how the plastic system was built. The module introduces life-cycle assessment "
            "methodology at a technical level, examines carbon accounting for plastics across "
            "their full lifecycle, and challenges students to interrogate whose interests are "
            "served by dominant recycling narratives."
        ),
        "age_group": "17+",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic origins", "fossil fuels", "political economy", "life-cycle assessment", "producer responsibility", "industrial history"]),
        "learning_outcomes": json.dumps([
            "Construct a historical account of how single-use plastic culture was deliberately engineered",
            "Apply life-cycle assessment methodology to calculate comparative environmental costs for two packaging materials",
            "Evaluate primary source documents for rhetorical strategy and vested interest",
            "Articulate a structural critique of recycling as the primary policy response to plastic pollution",
        ]),
        "pedagogical_approach": "critical inquiry",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 12, 13, 16]),
        "language": "en",
        "duration_per_module_minutes": 40,
        "duration_total_minutes": 200,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-story-17-plus",
        "is_free": 1,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "LCA Deep Dive — conduct a comparative lifecycle assessment for PET vs glass vs aluminium packaging across six impact categories",
            "Primary Source Analysis — annotate three industry documents from 1960–1990 and map the rhetorical strategies used to shift responsibility to consumers",
        ]),
        "discussion_prompts": json.dumps([
            "Is the plastic crisis primarily a failure of consumer behaviour, corporate strategy, or state regulation? Build an evidence-based argument.",
            "To what extent is recycling a technical solution to what is fundamentally a political problem?",
        ]),
    },

    # ── Module 2 · Ages 17+ ───────────────────────────────────────────────
    {
        "id": "plastic-m2-17-plus",
        "title": "Plastic Types & Recyclability (Ages 17+)",
        "description": "Examine the chemistry, economics, and politics behind why the global plastic recycling rate has never exceeded 10% — despite fifty years of trying.",
        "full_description": (
            "Students conduct a technical and political economy analysis of plastic recycling "
            "failure. The module covers polymer chemistry at a level appropriate for older "
            "students, including why mechanical recycling degrades polymer chains and why "
            "chemical recycling remains commercially unscalable at current technology levels. "
            "Students analyse commodity market data for secondary plastics, examine how virgin "
            "plastic pricing (subsidised through fossil fuel policy) undercuts recycled material "
            "markets, and evaluate the evidence on extended producer responsibility schemes "
            "in the EU, UK, and Canada. The module includes a critical appraisal of major "
            "brand sustainability claims using publicly available third-party data."
        ),
        "age_group": "17+",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic types", "recycling systems", "chemical recycling", "producer responsibility", "commodity markets", "greenwashing"]),
        "learning_outcomes": json.dumps([
            "Explain the chemical mechanisms that limit mechanical recycling of mixed plastic streams",
            "Assess the commercial viability of chemical recycling against current evidence",
            "Analyse how fossil fuel subsidies affect the economics of plastic recycling markets",
            "Evaluate an EPR scheme in a named jurisdiction against its stated objectives using available data",
        ]),
        "pedagogical_approach": "real-world trade-offs",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 12, 13, 17]),
        "language": "en",
        "duration_per_module_minutes": 40,
        "duration_total_minutes": 200,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-types-17-plus",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Market Analysis — track commodity price data for rPET, rHDPE, and virgin PET over five years and identify causal factors in price divergence",
            "EPR Scheme Audit — evaluate the French REP emballages scheme against its 2025 targets using published data",
        ]),
        "discussion_prompts": json.dumps([
            "If fossil fuel subsidies were eliminated tomorrow, what would happen to plastic recycling markets? Model the mechanism.",
            "Should chemical recycling count toward national recycling targets? What are the political stakes of that definitional choice?",
        ]),
    },

    # ── Module 3 · Ages 17+ ───────────────────────────────────────────────
    {
        "id": "plastic-m3-17-plus",
        "title": "Waste Systems & Infrastructure (Ages 17+)",
        "description": "Analyse waste management as a political and economic infrastructure system — from procurement models and gate fees to the global waste trade and environmental justice.",
        "full_description": (
            "This module provides a systems analysis of waste management infrastructure, "
            "covering procurement economics (public vs private, gate fees, landfill tax "
            "pass-through), MRF technology investment cycles, and the political economy of "
            "waste contracts. Students conduct a detailed case study of China's 2018 National "
            "Sword policy and model its downstream effects on collection, processing, and "
            "export markets in five countries. The module introduces environmental justice "
            "as an analytical lens — examining how waste burden distribution maps onto "
            "race, income, and geography — and evaluates the Basel Convention plastic "
            "amendments as an international legal instrument."
        ),
        "age_group": "17+",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["recycling systems", "waste infrastructure", "waste trade", "waste colonialism", "environmental justice", "Basel Convention", "policy"]),
        "learning_outcomes": json.dumps([
            "Model the downstream effects of China National Sword on waste markets in at least three countries using data",
            "Apply environmental justice frameworks to analyse the geographic distribution of waste infrastructure",
            "Evaluate the Basel Convention plastic waste amendments as a legal instrument — scope, enforcement, and gaps",
            "Compare privatised and municipally-operated waste management on cost, accountability, and environmental outcomes",
        ]),
        "pedagogical_approach": "critical inquiry",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 10, 11, 12, 16, 17]),
        "language": "en",
        "duration_per_module_minutes": 40,
        "duration_total_minutes": 200,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/waste-systems-17-plus",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "National Sword Impact Model — build a causal map tracing policy effects across five national waste systems",
            "Environmental Justice Mapping — plot MRF, landfill, and incinerator locations against census income and ethnicity data for a chosen urban area",
        ]),
        "discussion_prompts": json.dumps([
            "Is the global waste trade a form of environmental colonialism, or a legitimate mechanism for resource efficiency? What evidence would change your view?",
            "Should waste management be treated as a public good like water supply, or is market competition in the public interest? What does the evidence show?",
        ]),
    },

    # ── Module 4 · Ages 17+ ───────────────────────────────────────────────
    {
        "id": "plastic-m4-17-plus",
        "title": "Ocean Plastic & Ecosystems (Ages 17+)",
        "description": "Review the scientific evidence on ocean plastic impacts, critically evaluate cleanup and source-reduction interventions, and assess the global treaty landscape.",
        "full_description": (
            "Students engage with the primary scientific literature on ocean plastic — covering "
            "bioaccumulation pathways, endocrine disruption by plastic additives, microplastic "
            "ingestion across trophic levels, and the emerging evidence on nanoplastics in "
            "human tissue. The module critically evaluates ocean cleanup technology claims "
            "against peer-reviewed evidence, including bycatch data and cost-per-tonne "
            "comparisons with source-reduction alternatives. Students analyse the negotiating "
            "history of the UN Global Plastics Treaty and assess competing national positions, "
            "identifying structural barriers to an effective binding agreement."
        ),
        "age_group": "17+",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["ocean plastic", "microplastics", "nanoplastics", "marine ecosystems", "cleanup technology", "UN Plastics Treaty", "source reduction"]),
        "learning_outcomes": json.dumps([
            "Evaluate the scientific evidence for microplastic and nanoplastic impacts on human and ecosystem health",
            "Critically assess ocean cleanup technology using cost-effectiveness and unintended consequence data",
            "Analyse the negotiating dynamics of the UN Global Plastics Treaty and identify the main fault lines",
            "Compare upstream production caps with downstream cleanup as policy mechanisms using a cost-benefit framework",
        ]),
        "pedagogical_approach": "critical inquiry",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 13, 14, 16, 17]),
        "language": "en",
        "duration_per_module_minutes": 40,
        "duration_total_minutes": 200,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/ocean-plastic-17-plus",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Evidence Appraisal — rate the quality of evidence for five ocean cleanup technology claims using a structured appraisal tool",
            "Treaty Simulation — take a national negotiating position in the UN Plastics Treaty and prepare a position paper addressing production caps, liability, and financing",
        ]),
        "discussion_prompts": json.dumps([
            "Given the emerging nanoplastics evidence, should the precautionary principle require an immediate moratorium on new plastic production? What are the counter-arguments?",
            "Why have international plastic pollution negotiations repeatedly failed to agree on production caps? Identify the structural interests at play.",
        ]),
    },

    # ── Module 5 · Ages 17+ ───────────────────────────────────────────────
    {
        "id": "plastic-m5-17-plus",
        "title": "Circular Economy & Trade-offs (Ages 17+)",
        "description": "Stress-test circular economy theory against political economy, thermodynamic limits, and global trade rules — and design an intervention that could actually work.",
        "full_description": (
            "Students conduct a rigorous critique of circular economy frameworks, examining "
            "the thermodynamic limits of material cycling, the rebound effect, and whether "
            "circular economy represents a genuine systems paradigm shift or a legitimising "
            "narrative for continued growth. The module evaluates the Ellen MacArthur "
            "Foundation model, the EU Circular Economy Action Plan, and degrowth critiques "
            "side by side. Students analyse how international trade rules (WTO, RCEP, CPTPP) "
            "constrain national circular economy policy, and complete a capstone project: "
            "designing a binding plastic policy intervention, stress-testing it against "
            "industry, trade, and political constraints, and presenting it as a policy brief."
        ),
        "age_group": "17+",
        "availability": "available",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["circular economy", "degrowth", "policy design", "trade rules", "rebound effect", "systems thinking", "trade-offs"]),
        "learning_outcomes": json.dumps([
            "Apply thermodynamic constraints to evaluate the theoretical limits of circular economy",
            "Compare circular economy and degrowth frameworks and assess their political feasibility",
            "Identify specific WTO or regional trade agreement provisions that constrain circular economy policy",
            "Produce a structured policy brief for a plastic intervention in a named jurisdiction, including a stakeholder impact assessment",
        ]),
        "pedagogical_approach": "real-world trade-offs",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection", "activity"]),
        "sdg_alignment": json.dumps([4, 8, 10, 12, 13, 16, 17]),
        "language": "en",
        "duration_per_module_minutes": 40,
        "duration_total_minutes": 200,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/circular-economy-17-plus",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([
            "Framework Stress-Test — apply four critique lenses (thermodynamic, rebound, trade, power) to the Ellen MacArthur Foundation circular economy model",
            "Policy Brief — draft a 600-word policy intervention for a named jurisdiction, including evidence base, stakeholder map, and anticipated opposition",
        ]),
        "discussion_prompts": json.dumps([
            "Is a circular economy compatible with infinite economic growth, or does circularity require questioning the growth imperative itself?",
            "Which is more likely to achieve rapid plastic reduction: a binding international treaty, national regulation, or market-driven corporate action? Make the strongest case for each, then state your own position.",
        ]),
    },
]


def seed():
    init_db()
    conn = get_db()
    c = conn.cursor()

    all_lessons = LESSONS + LESSONS_6_9 + LESSONS_17_PLUS
    for lesson in all_lessons:
        c.execute("""
            INSERT OR REPLACE INTO lessons (
                id, title, description, full_description, age_group,
                availability, edition, price_home_usd, price_classroom_usd,
                waste_stream, topic_tags, learning_outcomes, pedagogical_approach,
                content_types, sdg_alignment, language, duration_per_module_minutes,
                duration_total_minutes, audience, url, is_free, credential_context,
                worksheet_descriptions, discussion_prompts
            ) VALUES (
                :id, :title, :description, :full_description, :age_group,
                :availability, :edition, :price_home_usd, :price_classroom_usd,
                :waste_stream, :topic_tags, :learning_outcomes, :pedagogical_approach,
                :content_types, :sdg_alignment, :language, :duration_per_module_minutes,
                :duration_total_minutes, :audience, :url, :is_free, :credential_context,
                :worksheet_descriptions, :discussion_prompts
            )
        """, lesson)

    conn.commit()
    conn.close()
    print(f"Seeded {len(all_lessons)} lessons.")


if __name__ == "__main__":
    seed()
