"""
Sample protocol knowledge base for the SwasthyaSathi demo.

IMPORTANT: These are simplified, general-guidance summaries written for a
hackathon demo only -- loosely modeled on the *structure* of public health
triage guidance (e.g. IMNCI-style danger-sign checklists), NOT verbatim
official text and NOT a substitute for real clinical protocols. Before any
real-world use, replace this file with the actual current guidelines from
the Ministry of Health & Family Welfare / your state health department, and
have a clinician review it.

Each entry is one retrievable "chunk" for the RAG pipeline. `source` is
shown back to the worker in the app for transparency -- so the response is
always traceable to *something*, never presented as the AI's own opinion.
"""

PROTOCOLS = [
    {
        "id": "infant-fever",
        "title": "Fever in infant under 6 months",
        "source": "Illustrative — modeled on IMNCI infant danger-sign checklist",
        "text": (
            "If an infant under 6 months has a fever and is not feeding well, "
            "is unusually drowsy, or feels hot to the touch for more than a day, "
            "this is a red-flag / urgent case. Advise the caregiver to go to the "
            "nearest Primary Health Centre (PHC) or hospital immediately. Do not "
            "wait to see if it improves. While arranging transport, keep the baby "
            "lightly dressed and continue breastfeeding if possible."
        ),
    },
    {
        "id": "child-diarrhea",
        "title": "Diarrhea in a young child",
        "source": "Illustrative — modeled on IMNCI diarrhea management checklist",
        "text": (
            "For a child with loose, watery stools multiple times a day but who is "
            "alert, drinking normally, and has no blood in the stool, this is "
            "usually manageable at home. Advise oral rehydration solution (ORS) "
            "after every loose stool, continued normal feeding, and hygiene "
            "precautions. Refer to a health facility if there is blood in the "
            "stool, repeated vomiting, sunken eyes, unusual sleepiness, or the "
            "child is unable to drink -- these are danger signs."
        ),
    },
    {
        "id": "pregnancy-swelling",
        "title": "Swelling in a pregnant woman",
        "source": "Illustrative — modeled on maternal danger-sign guidance",
        "text": (
            "Mild swelling in the feet and ankles in late pregnancy can be normal. "
            "However, swelling in the face and hands, combined with severe "
            "headache, blurred vision, or upper abdominal pain, are danger signs "
            "that may indicate a serious condition. Advise immediate referral to "
            "a health facility for blood pressure check and further evaluation. "
            "Do not tell the woman to simply rest and wait if these combined "
            "signs are present."
        ),
    },
    {
        "id": "newborn-not-feeding",
        "title": "Newborn refusing to feed",
        "source": "Illustrative — modeled on newborn danger-sign checklist",
        "text": (
            "A newborn (first 28 days) who is refusing to feed, feels cold to "
            "the touch, is unusually floppy, or has fast/difficult breathing "
            "requires urgent referral to a hospital with newborn care facilities. "
            "This age group can deteriorate quickly, so err on the side of "
            "referring rather than watchful waiting."
        ),
    },
    {
        "id": "cough-fast-breathing",
        "title": "Cough with fast breathing in a child",
        "source": "Illustrative — modeled on IMNCI pneumonia danger-sign checklist",
        "text": (
            "A child with cough and fast or labored breathing (chest moving in "
            "with each breath) may have pneumonia. This requires prompt referral "
            "to a health facility for assessment. A cough alone, without fast "
            "breathing or danger signs, and with the child otherwise active and "
            "feeding well, can usually be monitored at home with fluids and rest."
        ),
    },
    {
        "id": "snake-bite",
        "title": "Suspected snake bite",
        "source": "Illustrative — modeled on standard first-aid/referral guidance",
        "text": (
            "For a suspected snake bite: keep the person calm and still, "
            "immobilize the bitten limb at or below heart level, remove any "
            "tight jewelry or clothing near the bite, and arrange immediate "
            "transport to the nearest hospital. Do not cut the wound, do not "
            "apply a tight tourniquet, and do not attempt to suck out venom -- "
            "these traditional measures can cause more harm."
        ),
    },
    {
        "id": "elderly-confusion",
        "title": "Sudden confusion in an elderly person",
        "source": "Illustrative — modeled on stroke danger-sign guidance",
        "text": (
            "Sudden new confusion, slurred speech, weakness on one side of the "
            "body, or drooping of the face in an elderly person are possible "
            "signs of a stroke. This is a medical emergency -- advise immediate "
            "transport to the nearest hospital, noting the time the symptoms "
            "started, as this affects treatment options."
        ),
    },
    {
        "id": "malnutrition-check",
        "title": "Checking for child malnutrition",
        "source": "Illustrative — modeled on nutrition screening guidance",
        "text": (
            "Visible signs of possible severe malnutrition in a child include "
            "very thin arms and legs, visible rib outlines, or swelling in both "
            "feet. If any of these are seen, refer the child to a health "
            "facility or nutrition rehabilitation center for a full assessment "
            "rather than assessing at home."
        ),
    },
]
