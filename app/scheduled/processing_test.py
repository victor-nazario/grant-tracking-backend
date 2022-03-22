from processing import obtain_close_date
from datetime import datetime

test_description = "<![CDATA[ <TABLE BORDER=0 WIDTH='100%'><TR><TD><table><tr><td>Funding Opportunity ID: " \
                   "</td><td>323597</td></tr><tr><td>Opportunity Number: </td><td>20-538</td></tr><tr><td>Opportunity " \
                   "Title:</td><td>Linguistics Program - Doctoral Dissertation Research Improvement " \
                   "Grants</td></tr><tr><td>Opportunity Category:</td><td>Discretionary</td></tr><tr><td>Opportunity " \
                   "Category Explanation:</td><td></td></tr><tr><td valign='top'>Funding Instrument Type: " \
                   "</td><td>Grant</td></tr><tr><td valign='top'>Category of Funding Activity: </td><td>Science and " \
                   "Technology and other Research and Development</td></tr><tr><td valign='top'>Category Explanation: " \
                   "</td><td></td></tr><tr><td valign='top'>CFDA Number(s): </td><td>47.075</td></tr><tr><td " \
                   "valign='top'>Eligible Applicants:</td><td>Others (see text field entitled Additional Information " \
                   "on Eligibility for clarification)</td></tr><tr><td valign='top'>Additional Information on " \
                   "Eligibility:</td><td>*Who May Submit Proposals: Proposals may only be submitted by the following: " \
                   "-Institutions of Higher Education (IHEs) - Two- and four-year IHEs (including community colleges) " \
                   "accredited in, and having a campus located in the US, acting on behalf of their faculty " \
                   "members.Special Instructions for International Branch Campuses of US IHEs: If the proposal " \
                   "includes funding to be provided to an international branch campus of a US institution of higher " \
                   "education (including through use of subawards and consultant arrangements), the proposer must " \
                   "explain the benefit(s) to the project of performance at the international branch campus, " \
                   "and justify why the project activities cannot be performed at the US campus. *Who May Serve as " \
                   "PI: DDRI proposals must be submitted with a principal investigator (PI) and a co-principal " \
                   "investigator (co-PI). The PI must be the advisor of the doctoral student or another faculty " \
                   "member at the USIHE where the doctoral student is enrolled. The doctoral student must be a " \
                   "co-PI.</td></tr><tr><td valign='top'>Agency Code:</td><td>NSF</td></tr><tr><td " \
                   "valign='top'>Agency Name:</td><td>National Science Foundation</td></tr><tr><td>Posted " \
                   "Date:</td><td>Jan 11, 2020</td></tr><tr><td>Close Date:</td><td>Jul 15, " \
                   "2022 </td></tr><tr><td>Last Updated Date:</td><td>Feb 02, 2022</td></tr><tr><td>Award " \
                   "Ceiling:</td><td>$0</td></tr><tr><td>Award Floor:</td><td>$0</td></tr><tr><td>Estimated Total " \
                   "Program Funding:</td><td>$400,000</td></tr><tr><td>Expected Number of " \
                   "Awards:</td><td>35</td></tr><tr><td>Description:</td><td>The Linguistics Program supports basic " \
                   "science in the domain of human language, encompassing investigations of the grammatical " \
                   "properties of individual human languages, and of natural language in general. Research areas " \
                   "include syntax, linguistic semantics and pragmatics, morphology, phonetics, and phonology. The " \
                   "program encourages projects that are interdisciplinary in methodological or theoretical " \
                   "perspective, and that address questions that cross disciplinary boundaries, such as (but not " \
                   "limited to): What are the psychological processes involved in the production, perception, " \
                   "and comprehension of language? What are the computational properties of language and/or the " \
                   "language processor that make fluent production, incremental comprehension or rapid learning " \
                   "possible? How do the acoustic and physiological properties of speech inform our theories of " \
                   "language and/or language processing? What role does human neurobiology play in shaping the " \
                   "various components of our linguistic capacities? How does language develop in children? What " \
                   "social and cultural factors underlie language variation and change? The Linguistics Program does " \
                   "not make awards to support clinical research projects, nor does it support work to develop or " \
                   "assess pedagogical methods or tools for language instruction. DDRI proposals to document the " \
                   "linguistic properties of endangered languages should be submitted to the Dynamic Language " \
                   "Infrastructure (DLI-DDRI) Program: " \
                   "https://www.nsf.gov/pubs/2019/nsf19607/nsf19607.htm.</td></tr><tr><td>Version:</td><td>7</td></tr" \
                   "><tr><td>Modification Comments:</td><td>.</td></tr></table></TD></TR></TABLE> ]]> "


def test_obtain_close_date():
    assert type(obtain_close_date(test_description)) is datetime, "Expected returned value to be of type datetime"


if __name__ == '__main__':
    test_obtain_close_date()
