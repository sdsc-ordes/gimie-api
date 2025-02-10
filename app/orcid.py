# USER FLOW

# Download user html
from dataclasses import dataclass, asdict
import json
import re
import sys
from typing import Optional

from bs4 import BeautifulSoup
import requests
import argparse

@dataclass
class Organization:
    name: str
    country: str
    ror: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):

        ror = None
        try:
            org_id = data['disambiguated-organization']
            if org_id['disambiguation-source'] == 'ROR':
                ror = org_id['disambiguated-organization-identifier'] 
        except KeyError:
            # NOTE: if no ror id, we could also search org name using ROR API
            # but it would be error prone and slower.
            pass

        return Organization(
            name=data['name'],
            country=data['address']['country'],
            ror=ror,
        )

@dataclass
class Affiliation:
    organization: Organization
    start_year: Optional[int]
    end_year: Optional[int]

    @classmethod
    def from_dict(cls, data: dict):

        org = Organization.from_dict(data['organization'])
        get_date = lambda x: int(x['year']['value']) if x else None
        return cls(
            organization=org ,
            start_year=get_date(data['start-date']),
            end_year=get_date(data['end-date']),
        )

@dataclass
class OrcidRecord:
    educations: list[Affiliation]
    employments: list[Affiliation]

    @classmethod
    def from_url(cls, url: str):
        """Instantiate a record from an ORCiD API url"""
        response = requests.get(url, headers={'Accept': 'application/json'})
        return cls.from_dict(response.json())

    @classmethod
    def from_dict(cls, record_data: dict):
        """Instantiate a record from an ORCiD API json response"""
        employments = []
        educations = []
        activities = record_data['activities-summary']
        for group in activities['educations']['affiliation-group']:
            for edu in group['summaries']:
                educations.append(Affiliation.from_dict(edu['education-summary']))

        for group in activities['employments']['affiliation-group']:
            for employ in group['summaries']:
                employments.append(Affiliation.from_dict(employ['employment-summary']))
        

        return cls(
            educations=educations,
            employments=employments,
        )

    def __str__(self):
        """str conversion pretty-prints the record and all its members as indented json."""
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)



def get_orcid_from_github(username):
    """Extracts the ORCID link from a GitHub user's profile, restricted to the vcard section."""
    url = f"https://github.com/{username}"
    
    response = requests.get(url)
    # TODO retry (3x)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the vcard section
    
    vcard_section = soup.find("ul", attrs={"class": "vcard-details"})

    # Find all links within the vcard section
    links = vcard_section.find_all("a", href=True)
    
    # Search for ORCID link
    orcid_pattern = re.compile(r"https?://orcid\.org/\d{4}-\d{4}-\d{4}-\d{4}")
    for link in links:
        if orcid_pattern.match(link["href"]):
            return link["href"]
    
    return None


def fetch_orcid_record(orcid: str) -> OrcidRecord:
    url = f"https://pub.orcid.org/v3.0/{orcid}"
    print(url)
    return OrcidRecord.from_url(url)

def run_analysis_from_github_username(github_username):
    # Extract ORCID
    orcid_link = get_orcid_from_github(github_username)

    if orcid_link:
        print(f"ORCID Link found: {orcid_link}")
        orcid_id = orcid_link.removeprefix("https://orcid.org/")
        orcid_record = fetch_orcid_record(orcid_id)

        return orcid_record
    else:
        print("No ORCID link found on this profile.")
        return None

def run_analysis_from_orcid(orcid_link):
    print(f"ORCID Link found: {orcid_link}")
    orcid_id = orcid_link.removeprefix("https://orcid.org/")
    orcid_record = fetch_orcid_record(orcid_id)

    return orcid_record
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ORCID record from GitHub username.")
    parser.add_argument("github_username", type=str, help="GitHub username to extract ORCID from")
    args = parser.parse_args()

    github_username = args.github_username

    orcid_record = run_analysis_from_github_username(github_username)

    if not orcid_record:
        exit()