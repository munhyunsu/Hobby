/**
 * The event handler triggered when editing the spreadsheet.
 * @param {Event} e The onEdit event.
 */
function onEdit(e) {
  // Sleep
  var sleepTime = 5000;
  var lastEditedTime = new Date().getTime();
  PropertiesService.getScriptProperties().setProperty('lastEditedTime', lastEditedTime);
  Utilities.sleep(sleepTime);
  var newTime = new Date().getTime();
  if(newTime - PropertiesService.getScriptProperties().getProperty('lastEditedTime') < sleepTime - 50) {
    return;
  }
  
  // Check specific sheet
  var sheet = SpreadsheetApp.getActiveSheet();
  if(sheet.getName() !== '옐로카드') {
    return;
  }
  
  // Build rules
  var range = sheet.getRange("A1:A51");
  var rule1 = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEndsWith("+")
      .setBackground("#8EF691")
      .setRanges([range])
      .build();
  var rule2 = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEndsWith("-")
      .setBackground("#F68EE2")
      .setRanges([range])
      .build();
  var rules = [rule1, rule2];
  sheet.setConditionalFormatRules(rules);
}
