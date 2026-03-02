function fetchOptionChainFromServer() {
  const url = "https://your-app-name.onrender.com/nifty";
  const response = UrlFetchApp.fetch(url);
  const data = JSON.parse(response.getContentText());

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("OPTION_CHAIN");
  sheet.clear();
  sheet.appendRow(["Strike","CE OI","CE Chg OI","PE OI","PE Chg OI"]);

  data.forEach(row => {
    sheet.appendRow([
      row.strike,
      row.ce_oi,
      row.ce_change_oi,
      row.pe_oi,
      row.pe_change_oi
    ]);
  });
}
