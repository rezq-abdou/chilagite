function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var headers = sheet.getDataRange().getValues()[0] || [];
    
    var data = {
      timestamp: new Date(),
      name: e.parameter.name || '',
      phone: e.parameter.phone || '',
      wilaya: e.parameter.wilaya || '',
      municipality: e.parameter.municipality || '',
      delivery: e.parameter.delivery === 'office' ? 'توصيل للمكتب' : e.parameter.delivery === 'home' ? 'توصيل للمنزل' : (e.parameter.delivery || ''),
      qty: e.parameter.qty || '1'
    };

    var row = [];
    headers.forEach(function(h) {
      var key = h.toLowerCase().trim();
      if (key === 'الوقت' || key === 'time' || key === 'timestamp') row.push(data.timestamp);
      else if (key === 'الاسم' || key === 'name') row.push(data.name);
      else if (key === 'الهاتف' || key === 'phone') row.push(data.phone);
      else if (key === 'الولاية' || key === 'wilaya') row.push(data.wilaya);
      else if (key === 'البلدية' || key === 'municipality') row.push(data.municipality);
      else if (key === 'التوصيل' || key === 'delivery') row.push(data.delivery);
      else if (key === 'الكمية' || key === 'qty' || key === 'quantity') row.push(data.qty);
      else row.push('');
    });

    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ result: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'error', error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return doPost(e);
}
