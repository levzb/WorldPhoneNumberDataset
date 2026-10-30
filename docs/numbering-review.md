# Numbering review — 2026-10-30

## Scope and preservation

- All 1317 regional records and all 116 represented countries are retained, with the original per-file and per-country record counts. Duplicate places remain for compatibility.
- 122 four-field regional rows were repaired by restoring the missing `PrimaryCityOrNote` field. The same corrections are reflected in the combined CSV.
- Seven embedded header rows were removed from `AllCountries.csv`; they were not geographic records. It now contains one header and the unchanged number of actual regional records.
- 547 regional records had prefixes or location annotations corrected, including 542 prefix edits. This count includes repeated records across files.
- All 235 international entries were retained. Paraguay, already present in the regional data, was added to that reference file, giving 236 entries.
- The five-column regional schema and the original regional filenames remain unchanged.

The checks cover country calling codes, numeric prefixes, national lengths and fixed/mobile validity. Geographic associations were reviewed against available regulator tables and libphonenumber geocoding. This is a plausible-number dataset, not a subscriber directory or a complete city-allocation database.

## Important corrections

| Area | Correction | Source |
| --- | --- | --- |
| International reference | Quote the comma in Bonaire's name; remove spaces/commentary from code fields; add Paraguay; distinguish Norfolk Island's `+672` from mainland Australia's `+61`. | [ITU numbering plans](https://www.itu.int/oth/t0202), [metadata](https://github.com/google/libphonenumber/blob/v9.0.42/resources/PhoneNumberMetadata.xml) |
| Algeria | Correct Oran, Constantine, Batna, Blida and Tizi Ouzou. Prefer the regulator's allocation table over conflicting broad geocoder labels. | [ARPCE / Algérie Télécom table](https://www.arpce.dz/ar/file/w9k0q5) |
| Egypt | Correct Giza/Shubra, Luxor, Port Said, Damietta, Tanta, Ismailia and Faiyum. | [ITU Egypt plan](https://www.itu.int/oth/T020200003E/en) |
| Morocco | Replace mobile/incorrect one-digit city entries with fixed geographic prefixes. | [ANRT allocation table](https://www.anrt.ma/sites/default/files/Maroc_ANRT_Plan_national_numerotation.pdf) |
| Nigeria | Use current international fixed prefixes such as `201` for Lagos and `209` for Abuja, excluding the domestic trunk zero. | [NCC current allocations](https://ncc.gov.ng/operators/national-numbering-plan), [migration announcement](https://old.ncc.gov.ng/media-centre/news-headlines/1398-press-release-ncc-announces-change-to-fixed-lines-numbering-format) |
| Benin | Include the significant `01` added to the former eight-digit numbers. | [ARCEP Benin](https://arcep.bj/a-partir-de-30-novembre-2024-les-numeros-de-telephone-au-benin-passent-de-08-a-10-chiffres/) |
| Colombia | Use ten-digit national fixed numbers with `60` plus the regional identifier. Correct Bucaramanga and San Andrés as well. | [CRC migration notice](https://www.crcom.gov.co/es/noticias/comunicado-prensa/inicia-implementacion-definitiva-nuevo-esquema-numeracion-y-marcacion) |
| Zimbabwe | Use migrated regional/leading prefixes, including Harare, Bulawayo, Mutare, Gweru and Kwekwe. | [ITU bulletin 1164](https://www.ituob.org/issues/1164/) |
| Taiwan | Correct Changhua and Chiayi; preserve the different national lengths of geographic areas. | [ITU numbering table](https://www.ituob.org/issues/1261-en/) |
| Vietnam | Correct Can Tho, Hue, Bien Hoa, Vinh and Quy Nhon; retain established local ranges rather than treating proposed province-wide consolidation as a completed migration. | [Government numbering update](https://baochinhphu.vn/dieu-chinh-ma-vung-dien-thoai-co-dinh-sau-sap-xep-lai-tinh-thanh-pho-102250704124149458.htm) |
| United Kingdom | Correct incomplete Aberdeen and Swansea prefixes. | [Ofcom area-code lookup](https://www.ofcom.org.uk/phones-and-broadband/phone-numbers/telephone-area-codes-tool) |
| North America | Remove unrelated-city codes from several city rows, retain applicable overlays and remove repeated codes inside a field. This is not an exhaustive overlay list. | [NANPA reports](https://nanpa.com/reports/npa-reports), [Canadian numbering administrator maps](https://www.cnac.ca/area_code_maps/canadian_area_codes.htm) |
| Paraguay | Use official dialling prefixes for Capiatá, Villeta and Pedro Juan Caballero despite shorter, conflicting labels in geocoding data. | [Paraguayan embassy reference](https://www.embajadadeparaguay.ec/documentos/infoparaguay.pdf) |
| Other regions | Correct mismatched city prefixes across Africa, Asia, Europe, the Balkans and Latin America; replace prose describing code lengths with actual usable prefixes. | [Country-by-country references](country-review.csv), [versioned geocoding data](https://github.com/google/libphonenumber/tree/v9.0.42/resources/geocoding/en) |

Location annotations also correct the Equatorial Guinea/Libreville mix-up to Bata, Hongcheon to Hongseong within Chungcheongnam-do, Ravenna's region, several Bosnian administrative labels, and mislabeled capitals. These are corrections to existing records, not deletions of countries or regional rows.

## Approximate and non-geographic entries

`LocalAreaCode` is kept for compatibility, but its values are national leading prefixes. A prefix is not necessarily a separately dialled city code.

| Entries | Interpretation |
| --- | --- |
| Singapore, Hong Kong, Macau | National fixed-line ranges (`6`, `2/3`, `28` respectively), not city codes. The existing country-wide rows can serve a requested district. |
| Denmark | A non-geographic eight-digit plan. Retained prefixes are plausible examples; city labels do not determine the subscriber's location. [Danish authority](https://digst.dk/tele/telefoni-og-internet/numre/den-samlede-danske-nummerplan/) |
| France | Traditional regional prefixes remain useful examples, but geographic constraints on mainland `01`–`05` numbers were lifted in 2023. [ARCEP](https://www.arcep.fr/mes-demarches-et-services/consommateurs/fiches-pratiques/fin-du-decoupage-geographique-des-numeros-fixes-les-nouvelles-regles-en-vigueur.html) |
| Kuwait and Rwanda | National fixed-line leading ranges are retained without asserting a distinct code for each city. |
| Chad | A validated national mobile range replaces unsupported purported city codes. |
| Sudan | Khartoum/Omdurman use fixed prefixes; Port Sudan, Nyala and Kassala use a national mobile fallback rather than unconfirmed fixed city codes. |
| Democratic Republic of the Congo | Existing valid national mobile prefixes remain. They identify ranges, not city allocations. |
| Mali / Ségou | A national mobile fallback is used because the local fixed allocation could not be reconciled with current validation metadata; a Koulikoro fixed prefix is not presented as Ségou's code. |
| Liberia | Broad national fixed prefixes remain; exact locality allocation is unverified. The original place name `Glu` is retained and remains unverified. |
| Senegal | `338` represents Dakar and `339` the wider outside-Dakar region; individual towns are not distinguished. |
| Country-wide blank-place rows, and `Other regions` | Real national/representative prefixes replace dashes or descriptions of code lengths. They do not establish a new geographic allocation. |

## International identifiers

`code` is the E.164 country calling code: NANP territories therefore share `+1`. The `iso` column follows libphonenumber region identifiers, mostly ISO 3166-1 alpha-2; `AC`, `TA` and `XK` are special cases. Ascension and Tristan da Cunha are distinguished from the main Saint Helena entry.

The existing `Australia (External Territories)` name is retained, but its `NF` identifier narrows this row to Norfolk Island. It is not a claim that every Australian external territory uses `+672`. The separate British Indian Ocean Territory / Diego Garcia alias records are intentionally retained.

## Reproducible checks and limits

The generator and validator use the pinned Python port, [phonenumbers 9.0.42](https://github.com/daviddrysdale/python-phonenumbers/tree/v9.0.42), based on [Google libphonenumber](https://github.com/google/libphonenumber/tree/v9.0.42). All 1006 distinct country/prefix pairs are sampled with two fixed seeds and checked for correct country, significant prefix, length and fixed/mobile type. Integration tests cover the reported classes of errors and lookup behavior. All checks run offline after dependency installation.

These checks establish plausibility under the metadata, not that every random subscriber suffix is currently allocated. Portability, operator coverage, historic regional boundaries and incomplete geocoding mean that exact city ownership remains approximate. Refer to the linked regulator material for allocation-sensitive use.
