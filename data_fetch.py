import requests
import pandas as pd

def fetch_cve_data(results_per_page=50, start_index=0):
    """
    Fetch CVE data from NVD API and return as DataFrame.
    """
    url = (
        f"https://services.nvd.nist.gov/rest/json/cves/2.0"
        f"?resultsPerPage={results_per_page}&startIndex={start_index}"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Flatten JSON
    df = pd.json_normalize(data['vulnerabilities'])

    # Try to extract severity from CVSS v3 first, fallback to v2
    def get_severity(row):
        try:
            return row['cve.metrics.cvssMetricV31'][0]['cvssData']['baseSeverity']
        except (KeyError, IndexError, TypeError):
            try:
                return row['cve.metrics.cvssMetricV2'][0]['cvssData']['baseSeverity']
            except (KeyError, IndexError, TypeError):
                return None

    # Build cleaned DataFrame
    cleaned = pd.DataFrame({
        "CVE_ID": df['cve.id'],
        "Description": df['cve.descriptions'].apply(lambda d: d[0]['value'] if isinstance(d, list) and d else None),
        "PublishedDate": df['cve.published'],
        "Severity": df.apply(get_severity, axis=1)
    })

    return cleaned

def save_to_csv(df, filename="cve_data.csv"):
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(df)} CVEs to {filename}")

if __name__ == "__main__":
    df = fetch_cve_data(results_per_page=100)
    save_to_csv(df)
