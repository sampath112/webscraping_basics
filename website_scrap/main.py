from bs4 import BeautifulSoup
import requests
import time

# Add realistic headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def fetch_jobs():
    print("Fetching jobs...")

    url = 'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=python&cboWorkExp1=-1&txtLocation='

    # Make request with headers
    response = requests.get(url, headers=headers)

    # Optional: Check if request was successful
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        exit()

    # Get user input for unfamiliar skill
    unfamiliar_skill = input('Enter a skill you are not familiar with: ')
    print(f'Filtering out jobs that require {unfamiliar_skill}')

    html_text = response.text

    # Optional: Debug - uncomment to see what you actually received
    # print(html_text[:1000])  # Print first 1000 chars to check content

    soup = BeautifulSoup(html_text, 'lxml')

    # ✅ Use CSS selector (ignores spacing issues)
    jobs = soup.select('li > div.srp-listing.clearfix')

    # Or if you prefer find_all, fix the class string (two spaces, no trailing space):
    # jobs = soup.find_all('div', class_='srp-listing  clearfix')  # Note: target <div>, not <li>

    print(f"✅ Found {len(jobs)} jobs")

    # Print first 3 job titles as a test
    for i, job in enumerate(jobs[:3], 1):
        title_tag = job.find('h3')
        company_tag = job.find('span', class_='srp-comp-name')
        if title_tag and company_tag:
            title = title_tag.get_text(strip=True)
            company = company_tag.get_text(strip=True)
            print(f"{i}. {title} at {company}")

    for job in jobs:
            exp_text = job.find('div', class_='srp-exp').text.strip()  # e.g. "3 - 6 Years"
            min_exp = int(exp_text.split(' - ')[0])  # Extract "3"

            if min_exp > 1:  # ✅ Now it works!
            
                
                company = job.find('span', class_='srp-comp-name').text.strip()
                #skills = job.find('div', class_='srp-keyskills').text.replace(' ', ' ,').strip()
                skills_tags = job.find_all('a', class_='srphglt')  # Only anchor tags (ignore <span>)
                skills_list = [skill.get_text(strip=True) for skill in skills_tags]
                skills = ", ".join(skills_list)
                more_info = job.find('h3').find('a')['href']  # ✅ Gets the correct job detail link
                title = job.find('h3').text.strip()
                time_posted = job.find('span', class_='posting-time').text
                print('---')
                if unfamiliar_skill not in skills:
                    with open(f'posts/{title}.txt', 'w') as f:
                        f.write(f'Company Name: {company.strip()}\n')
                        f.write(f'Required Skills: {skills.strip()}\n')
                        f.write(f'Experience: {exp_text.strip()}\n')
                        f.write(f'More Info: {more_info}\n')
                        f.write(f'Time Posted: {time_posted}\n')
                    print(f'''
                        Job Title: {title}
                        Company: {company}
                        Required Skills: {skills}
                        time Posted: {time_posted}
                        Experience: {exp_text}
                        More Info: {more_info}  ''')
        

if __name__ == '__main__':
     while True:
        fetch_jobs()
        print('Waiting for 10 minutes...')
        
        time.sleep(600)  # Wait for 10 minutes before fetching again





# # Print all jobs with details

# for i, job in enumerate(jobs, 1):
#     # Job Title
#     title_tag = job.find('h3')
#     title = title_tag.get_text(strip=True) if title_tag else "N/A"

#     # Company Name
#     company_tag = job.find('span', class_='srp-comp-name')
#     company = company_tag.get_text(strip=True) if company_tag else "N/A"

#     # Experience
#     exp_tag = job.find('div', class_='srp-exp')
#     experience = exp_tag.get_text(strip=True) if exp_tag else "N/A"

#     # Location
#     loc_tag = job.find('div', class_='srp-loc')
#     location = loc_tag.get_text(strip=True) if loc_tag else "N/A"

#     # Salary
#     sal_tag = job.find('div', class_='srp-sal')
#     salary = sal_tag.get_text(strip=True) if sal_tag else "N/A"

#     # Key Skills
#     skills_tags = job.find_all('a', class_='srphglt')  # Only anchor tags (ignore <span>)
#     skills = [skill.get_text(strip=True) for skill in skills_tags]
#     skills_text = ", ".join(skills[:5]) + ("..." if len(skills) > 5 else "")  # Show first 5

#     # Print nicely
#     print(f"{'='*80}")
#     print(f"{i}. {title}")
#     print(f"   🏢 {company}")
#     print(f"   📍 {location}")
#     print(f"   ⏳ {experience} | 💰 {salary}")
#     print(f"   🔑 Skills: {skills_text}")
