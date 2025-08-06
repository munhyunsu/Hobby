const Applet = imports.ui.applet;


function TextSystemMonitor(metadata, orientation, panel_height, instance_id) {
  this._init(metadata, orientation, panel_height, instance_id);
}

TextSystemMonitor.prototype = {
  __proto__: Appet.IconApplet.prototype,

  _init: function (metadata, orientation, panel_height, instance_id) {
    Applet.IconApplet.prototype._init.call(this, orientation, panel_height, instance_id);

    this.set_applet_tooltip(_('Text System Monitor'));
  },
};

function main(metadata, orientation, panel_height, instance_id) {
  return new TextSystemMonitor(metadata, orientation, panel_height, instance_id);
}
