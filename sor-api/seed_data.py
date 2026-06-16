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

COMING_SOON = [
    {
        "id": "plastic-m1-6-9",
        "title": "The Plastic Story (Ages 6–9)",
        "description": "A gentle introduction to where plastic comes from and why we use so much of it — told through stories and simple activities.",
        "full_description": "Coming soon — this age group is currently in development.",
        "age_group": "6-9",
        "availability": "coming_soon",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic origins", "everyday plastic"]),
        "learning_outcomes": json.dumps([]),
        "pedagogical_approach": "systems thinking",
        "content_types": json.dumps(["video", "activity"]),
        "sdg_alignment": json.dumps([4, 12]),
        "language": "en",
        "duration_per_module_minutes": 15,
        "duration_total_minutes": 75,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-story-6-9",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([]),
        "discussion_prompts": json.dumps([]),
    },
    {
        "id": "plastic-m1-17-plus",
        "title": "The Plastic Story (Ages 17+)",
        "description": "An advanced exploration of plastic systems, political economy, and structural levers for change — aimed at older students and adult learners.",
        "full_description": "Coming soon — this age group is currently in development.",
        "age_group": "17+",
        "availability": "coming_soon",
        "edition": "both",
        "price_home_usd": 37,
        "price_classroom_usd": 147,
        "waste_stream": "plastic",
        "topic_tags": json.dumps(["plastic origins", "political economy", "systemic change"]),
        "learning_outcomes": json.dumps([]),
        "pedagogical_approach": "critical inquiry",
        "content_types": json.dumps(["video", "worksheet", "discussion_prompt", "reflection"]),
        "sdg_alignment": json.dumps([4, 12, 13]),
        "language": "en",
        "duration_per_module_minutes": 40,
        "duration_total_minutes": 200,
        "audience": "both",
        "url": "https://schoolofrecycling.com/courses/plastic-story-17-plus",
        "is_free": 0,
        "credential_context": json.dumps(["UNEP GPML member", "UN Global Compact"]),
        "worksheet_descriptions": json.dumps([]),
        "discussion_prompts": json.dumps([]),
    },
]


def seed():
    init_db()
    conn = get_db()
    c = conn.cursor()

    all_lessons = LESSONS + COMING_SOON
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
