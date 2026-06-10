# NoWhere Maps

**Satirical Google Maps-style reviews for real environmental phenomena that have no address.**

A [School of Recycling](https://www.schoolofrecycling.com) project.

---

## What is this?

NoWhere Maps reviews real environmental problems — plastic gyres, atmospheric CO₂, microplastics in human blood, forever chemicals in tap water — as if they were Google Maps listings.

Each location:
- Is a real, documented phenomenon with scientific sources
- Has no fixed address, but is pinned as close as possible to a meaningful real-world location
- Includes a deadpan review, a star rating, and a note explaining why that pin was chosen
- Is tagged by category (Ocean & water, Atmosphere, Soil & land, Corporate, Policy & greenwashing) and waste type (Plastic, Organic, Textile, E-waste, Mixed)

The recurring footer on every listing: *"Could not find this location on Google Maps. It found me."*

---

## Live site

[schoolofrecycling.com/nowhere-maps](https://www.schoolofrecycling.com/nowhere-maps)

---

## How to add locations

All locations live in a single array at the top of `index.html`. Each entry looks like this:

```javascript
{
  name: "Location name",
  type: "Short descriptor · Region",
  address: "No fixed address · Context · Detail",
  stars: 1,  // 1 to 5
  category: "Ocean & water",  // see categories below
  wasteType: "Plastic",       // see waste types below
  reviewShort: "One-line teaser shown in the list.",
  reviewFull: "Full paragraph review. Deadpan. Specific. Data-backed where possible.",
  sig: "— Posted from: [location]",
  pinNote: "Why this specific pin was chosen. One to three sentences.",
  lat: 0.0000,
  lng: 0.0000,
  tags: ["tag one", "tag two", "tag three"]
}
```

**Categories:** `Ocean & water` · `Atmosphere` · `Soil & land` · `Corporate` · `Policy & greenwashing`

**Waste types:** `Plastic` · `Organic` · `Textile` · `E-waste` · `Mixed`

To find coordinates: go to Google Maps, right-click any location, the lat/lng appears at the top of the context menu.

---

## Contributing

Fork the repo, add locations, submit a pull request.

Good additions:
- Real, documented phenomena with verifiable sources
- Specific — a named factory, river, research station, or event rather than a vague region
- Deadpan tone — the format works because it's matter-of-fact, not outraged
- Something that doesn't already have a Google Maps listing

Please keep the SoR credit in the footer of the HTML file.

---

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — free for NGO, media, editorial, and personal use. Commercial use requires a license. Contact: mmmhuizing@gmail.com

---

## About School of Recycling

[School of Recycling](https://www.schoolofrecycling.com) is an online K–12 waste and plastic literacy platform. NoWhere Maps is a free public tool and content series built to make waste systems education shareable and occasionally funny.
