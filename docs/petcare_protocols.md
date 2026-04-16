# PetCare Medellin Clinical Protocols

## Purpose

This document defines the first-line clinical guidance used by PetCare Medellin to triage common incoming requests from pet owners. It is intended for informational support and internal automation. It does not replace direct veterinary evaluation.

## Triage Levels

### Level 1: Immediate Emergency

Cases in this level must be escalated immediately to the on-duty veterinarian and should never remain in a standard queue.

Common signs:
- Difficulty breathing
- Convulsions or seizures
- Loss of consciousness
- Active bleeding that does not stop
- Suspected poisoning
- Severe trauma after falls, vehicle accidents, or bites
- Inability to stand with signs of distress
- Extreme abdominal swelling with pain
- Repeated vomiting with lethargy in puppies or kittens

Immediate instruction to pet owner:
- Go to the clinic immediately or to the nearest emergency veterinary center if the clinic is closed.
- Do not administer human medication unless previously instructed by a veterinarian.
- If poisoning is suspected, bring the product container or take a photo of the label.

Automation rule:
- Category: URGENCIA
- Priority: ALTA
- Escalation channel: direct Telegram alert to veterinarian on duty

### Level 2: Same-Day Clinical Attention

Cases in this level require prompt scheduling or callback the same day, but may not require emergency activation.

Common signs:
- Vomiting more than twice in 12 hours without collapse
- Diarrhea with blood but stable consciousness
- Refusal to eat for more than 24 hours
- Limping with pain
- Eye inflammation or discharge
- Fever reported by owner
- Ear pain, shaking head, or foul odor from ears
- Persistent coughing

Automation rule:
- Category: CONSULTA or AGENDAMIENTO depending on intent
- Priority: MEDIA
- Action: clinical guidance plus scheduling recommendation

### Level 3: Routine Attention

Cases in this level can usually be addressed with scheduling, administrative guidance, or documented clinical answers.

Common examples:
- Vaccination planning
- Deworming schedule
- Routine checkups
- Nutrition guidance
- Sterilization information
- Bathing or grooming questions
- Certificate requests

Automation rule:
- Category: AGENDAMIENTO, CONSULTA, or ADMINISTRATIVA
- Priority: BAJA or MEDIA depending on context

## Vaccination Guidance

### Dogs

Puppy vaccination usually starts at 6 to 8 weeks of age, followed by boosters according to veterinary guidance. Rabies vaccination is typically applied according to local legal and medical schedules.

Owner guidance:
- Bring previous vaccination card if available.
- Avoid exposing incomplete-vaccination puppies to high-risk environments.
- If the puppy has vomiting, diarrhea, or fever on the day of the appointment, the veterinarian must evaluate before vaccination.

### Cats

Kitten vaccination usually begins around 8 weeks of age with boosters as advised by the clinic.

Owner guidance:
- Indoor cats may still require preventive vaccination.
- If the cat is stressed or aggressive, inform the clinic before the appointment.

## Deworming Guidance

General preventive deworming depends on species, age, weight, and lifestyle.

Owner guidance:
- Do not administer over-the-counter products without confirming the correct dose.
- Report vomiting, diarrhea, visible parasites, or weight loss.
- Puppies and kittens may require a more frequent schedule than adult pets.

## Sterilization Guidance

Before surgery:
- The clinic must confirm fasting instructions
- The owner must report any previous illness or medication
- A pre-surgical evaluation may be required

After surgery:
- The pet must wear protective collar if indicated
- The incision must be kept clean and dry
- The owner must watch for swelling, discharge, bleeding, or opening of sutures

Escalation signs after surgery:
- Persistent vomiting
- Heavy bleeding
- Difficulty breathing
- Severe lethargy
- Wound opening

Automation rule:
- Post-surgical warning signs should be classified as SEGUIMIENTO or URGENCIA depending on severity

## Digestive Symptoms Guidance

Mild digestive symptoms may be observed temporarily, but red flags require escalation.

Low-risk scenario:
- One isolated episode of vomiting
- Mild soft stool without blood
- Normal energy

Red flags:
- Blood in stool or vomit
- More than three vomiting episodes in a day
- Lethargy
- Refusal to drink water
- Symptoms in very young or senior pets

Automation hint:
- If red flags are present, prioritize CONSULTA with MEDIA or URGENCIA with ALTA depending on severity

## Dermatology Guidance

Common issues:
- Itching
- Hair loss
- Red skin
- Ear scratching
- Skin odor

Owner guidance:
- Do not apply human creams without veterinary approval.
- If the pet has facial swelling, breathing changes, or rapidly worsening rash, escalate immediately.

## Dental Guidance

Common signs:
- Bad breath
- Difficulty chewing
- Gum bleeding
- Broken tooth

Automation hint:
- Broken tooth with active pain may require same-day attention.
- Routine cleaning requests are AGENDAMIENTO.

## Closing Rule for Automated Assistants

If the message indicates danger, rapid deterioration, intense pain, trauma, poisoning, seizures, or respiratory difficulty, the assistant must prioritize safety and escalate immediately.
