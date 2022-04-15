from app.scheduled.layers.processing import obtain_close_date, erase_b_tags
from datetime import datetime
import unittest

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

test_description_contains_extra_wording = "<![CDATA[ <TABLE BORDER=0 WIDTH='100%'><TR><TD><table><tr><td>Funding " \
                                          "Opportunity ID: </td><td>323740</td></tr><tr><td>Opportunity Number: " \
                                          "</td><td>2020-NIST-MEP-MDAP-01</td></tr><tr><td>Opportunity " \
                                          "Title:</td><td>NIST MEP Disaster Assessment " \
                                          "Program</td></tr><tr><td>Opportunity " \
                                          "Category:</td><td>Discretionary</td></tr><tr><td>Opportunity Category " \
                                          "Explanation:</td><td></td></tr><tr><td valign='top'>Funding Instrument " \
                                          "Type: </td><td>Cooperative Agreement</td></tr><tr><td " \
                                          "valign='top'>Category of Funding Activity: </td><td>Other (see text field " \
                                          "entitled Explanation of Other Category of Funding Activity for " \
                                          "clarification)</td></tr><tr><td valign='top'>Category Explanation: " \
                                          "</td><td>Manufacturing Extension Program</td></tr><tr><td " \
                                          "valign='top'>CFDA Number(s): </td><td>11.611</td></tr><tr><td " \
                                          "valign='top'>Eligible Applicants:</td><td>Others (see text field entitled " \
                                          "Additional Information on Eligibility for clarification)</td></tr><tr><td " \
                                          "valign='top'>Additional Information on Eligibility:</td><td>Eligible " \
                                          "applicants for this funding opportunity are recipients of current MEP " \
                                          "Center cooperative agreements. A MEP Center recipient may work " \
                                          "individually or may include proposed subawards to other recipients of MEP " \
                                          "Center cooperative agreements and/or proposed contracts with other " \
                                          "organizations as part of the applicant&#8217;s proposal, effectively " \
                                          "forming a team or consortium. A MEP Center may only submit one funding " \
                                          "application for each FEMA Disaster Declaration and, where an application " \
                                          "is submitted with respect to a particular FEMA Disaster Declaration, " \
                                          "such MEP Center may not be included as a subawardee or as a project " \
                                          "participant in any other applications pertaining to the same FEMA Disaster " \
                                          "Declaration. Moreover, a MEP Center that does not submit a funding " \
                                          "application for a particular FEMA Disaster Declaration may only be " \
                                          "included as a subawardee or as a project participant in one funding " \
                                          "application for each FEMA Disaster Declaration.</td></tr><tr><td " \
                                          "valign='top'>Agency Code:</td><td>DOC-NIST</td></tr><tr><td " \
                                          "valign='top'>Agency Name:</td><td>Department of Commerce<br>National " \
                                          "Institute of Standards and Technology</td></tr><tr><td>Posted " \
                                          "Date:</td><td>Jan 17, 2020</td></tr><tr><td>Close Date:</td><td>Apr 01, " \
                                          "2023 Applications for funding pursuant to this NOFO must be received by " \
                                          "NIST no later than 60 calendar days following the date that a Major or an " \
                                          "Emergency Disaster Declaration is declared by the Federal Emergency " \
                                          "Management Agency (FEMA Disaster Declaration) for all or a portion of an " \
                                          "impacted State or of Puerto Rico. NIST expects to complete its review, " \
                                          "selection of successful applicants, and award processing within 90 " \
                                          "calendar days of application receipt. This program is open, " \
                                          "and applications will be accepted by NIST on a rolling basis based on the " \
                                          "date of the subject FEMA Disaster Declaration and subject to the " \
                                          "publication of a superseding NOFO. See Section IV.4. in the Full " \
                                          "Announcement Text of this NOFO.</td></tr><tr><td>Last Updated " \
                                          "Date:</td><td>Feb 24, 2022</td></tr><tr><td>Award " \
                                          "Ceiling:</td><td>$0</td></tr><tr><td>Award " \
                                          "Floor:</td><td>$0</td></tr><tr><td>Estimated Total Program " \
                                          "Funding:</td><td></td></tr><tr><td>Expected Number of " \
                                          "Awards:</td><td></td></tr><tr><td>Description:</td><td>NIST invites " \
                                          "applications from current recipients of Manufacturing Extension " \
                                          "Partnership Center cooperative agreements (MEP Centers) to perform " \
                                          "assessments of small- and medium-sized manufacturers (SMMs) in areas " \
                                          "subject to a FEMA Disaster Declaration. These assessments should be " \
                                          "designed to identify the impact, if any, to the operations of the SMMs as " \
                                          "result of the subject disaster. MEP Centers receiving funding pursuant to " \
                                          "this program must also assist impacted SMMs in identifying and accessing " \
                                          "Federal, State and local resources to aid in business recovery efforts " \
                                          "and, as appropriate, in the development of a risk mitigation plan for " \
                                          "future disasters. Award recipients will further be required to share the " \
                                          "results of their project, including disaster preparedness lessons learned " \
                                          "and SMMs best practices, with other SMMs, NIST and the MEP National " \
                                          "NetworkTM in order to help the SMM community with future disaster " \
                                          "resilience planning efforts. See Section I. in the Full Announcement Text " \
                                          "of this " \
                                          "NOFO.</td></tr><tr><td>Version:</td><td>4</td></tr><tr><td>Modification " \
                                          "Comments:</td><td>Update to close " \
                                          "date.</td></tr></table></TD></TR></TABLE> ]]> "

test_values = [test_description, test_description_contains_extra_wording]


class PersistenceTestCase(unittest.TestCase):

    def test_obtain_close_date(self):
        for value in test_values:
            assert type(obtain_close_date(value)) is datetime, "Expected returned value to " \
                                                               "be of type datetime "

    def test_erase_b_tags(self):
        tag1 = '<b>O-OJJDP-2022-171251</b>'
        result_tag1 = erase_b_tags(tag1)
        self.assertEquals(result_tag1, 'O-OJJDP-2022-171251')

