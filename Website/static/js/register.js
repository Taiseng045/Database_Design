document.addEventListener("DOMContentLoaded", function () {
  function fillSameAsBirthPlace() {
    const isChecked = document.getElementById("sameAsBirthPlace").checked;

    // Example values from the Birth Place fields
    const birthProvince = document.getElementById("bCity").value;
    const birthDistrict = document.getElementById("bDistrict").value; // Example District
    const birthCommune = document.getElementById("bCommune").value;
    const birthVillage = document.getElementById("bVillage").value; // Example Commune
    const birthStreet = document.getElementById("bStreetAdd").value; // Example Street
    const birthPostalCode = document.getElementById("bPostal").value; // Example Postal Code
    const birthCountry = document.getElementById("bCountry").value;

    if (isChecked) {
      // Fill the current address fields with the birth place values
      document.getElementById("currentCity").value = birthProvince;
      document.getElementById("cDistrict").value = birthDistrict; // Corrected ID here
      document.getElementById("cCommune").value = birthCommune;
      document.getElementById("cStreetAdd").value = birthStreet;
      document.getElementById("cVillage").value = birthVillage;
      document.getElementById("cPostal").value = birthPostalCode;
      document.getElementById("cCountry").value = birthCountry;
    } else {
      // Clear the current address fields if unchecked
      document.getElementById("currentCity").value = "";
      document.getElementById("cDistrict").value = ""; // Corrected ID here
      document.getElementById("cCommune").value = "";
      document.getElementById("cStreetAdd").value = "";
      document.getElementById("cVillage").value = "";
      document.getElementById("cPostal").value = "";
      document.getElementById("cCountry").value = "";
    }
  }

  // Add event listener for the checkbox
  document
    .getElementById("sameAsBirthPlace")
    .addEventListener("change", fillSameAsBirthPlace);
});
document.addEventListener("DOMContentLoaded", function () {
  function fetchCaseDetails() {
    const caseNumber = document.getElementById("caseNumber").value; // Get case number from input
    console.log(caseNumber);
    if (caseNumber) {
      // Send GET request to fetch case details
      fetch(`/get_case_fill?case_number=${caseNumber}`)
        .then((response) => response.json())
        .then((result) => {
          console.log(result);
          if (!result.found) {
            // case number does not exist in DB — treat as new case
            console.log("New case number. No data found.");
            return; // let user fill in manually
          }
            const arrestDate = data[3];
            const formattedDate = convertToDateString(arrestDate);
            let arrestTime = data[14]; // Example: '9:45:00'
            arrestTime = formatTime(arrestTime);
            document.getElementById("caseType").value = data[1];
            document.getElementById("caseStatus").value = data[2];
            document.getElementById("caseArrestDate").value = formattedDate;
            document.getElementById("caseArrestTime").value = arrestTime;
            document.getElementById("caseArrestingOfficer").value = data[4];
            document.getElementById("caseDescription").value = data[11];
            document.getElementById("CLcity").value = data[5];
            document.getElementById("CLdistrict").value = data[6];
            document.getElementById("CLcommune").value = data[7];
            document.getElementById("CLvillage").value = data[8];
            document.getElementById("CLstreetAdd").value = data[9];
            document.getElementById("CLcountry").value = data[10];
        })
        .catch((error) => {
          console.error("Error:", error); // Log any errors in the fetch operation
        });
    }
  }

  // Event listener for Case Number input
  document
    .getElementById("caseNumber")
    .addEventListener("input", fetchCaseDetails);
});
function convertToDateString(dateString) {
  const date = new Date(dateString); // Convert full date string to Date object
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Months are zero-indexed
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`; // Return in YYYY-MM-DD format
}
function formatTime(time) {
  // Split the time into hours, minutes, and seconds
  let timeParts = time.split(":");
  let hours = timeParts[0].padStart(2, "0");
  let minutes = timeParts[1].padStart(2, "0");
  let seconds = timeParts[2] || "00"; // If no seconds provided, default to '00'

  // Return the formatted time in HH:mm:ss
  return `${hours}:${minutes}:${seconds}`;
}
