/**
 * The event handler triggered when editing the spreadsheet.
 * @param {Event} e The onEdit event.
 */
function onEdit(e) {
  // Sleep
  var sleepTime = 10000;
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
  
  // Build rules for Name coloring
  var range = sheet.getRange("A1:A51");
  range.setBackground("#FFFFFF");
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
  
  // Build rules
  var range = sheet.getRange("B2:B51");
  range.setBackground("#FFFFFF");
  range.setValue("=IF(COUNTA(INDIRECT(ADDRESS(ROW(),COLUMN()+2)&\":\"&ADDRESS(ROW(),COLUMN()+4)))>0, \"Good\", \"Bad\")");
  var rule3 = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo("Good")
      .setBackground("#DAF7A6")
      .setRanges([range])
      .build();
  var rule4 = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo("Bad")
      .setBackground("#FFC300")
      .setRanges([range])
      .build();
  var rules = [rule1, rule2, rule3, rule4];
  sheet.setConditionalFormatRules(rules);
}
