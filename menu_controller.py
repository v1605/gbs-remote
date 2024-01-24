import vga2_bold_16x32 as font
import vga2_8x16 as small_font
import utime
import st7789
import tft_buttons
import machine

class MenuItem:

    def __init__(self, display, item_id):
        self.id = item_id
        self.display = display

class MenuController():
    
    def __init__(self, tft, gbs_api):
        self._tft = tft
        self._options = []
        self._display_options = []
        self._page = 0
        self._info=False
        self._buttons = tft_buttons.Buttons()
        self.enable_buttons()
        self._gbs_api = gbs_api
        self.ip = ""
        self.loading_increment = 10;
    
    def enable_buttons(self):
        self._buttons.key0.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self._menu_button_handler(0))
        self._buttons.key1.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self._menu_button_handler(1))
        self._buttons.key2.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self._menu_button_handler(2))
        self._buttons.key3.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self._menu_button_handler(3))
        self._buttons.up.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self.next_page())
        self._buttons.down.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self.previous_page())
        self._buttons.left.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self.toogle_info())
        self._buttons.right.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self.toogle_info())
        self._buttons.center.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: self.reload_options())
          
    def disable_buttons(self):
        self._buttons.key0.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.key1.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.key2.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.key3.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.up.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.down.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.left.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.right.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        self._buttons.center.irq(trigger=machine.Pin.IRQ_FALLING, handler = lambda t: None)
        
    def reload_options(self):
        self._options = self._gbs_api.load_options()
        self.set_page(0)
        if len(self._options) == 0:
            self._tft.fill(st7789.BLACK)
            self._tft.text(small_font,"No options",15,20,st7789.WHITE,st7789.BLACK)
            self._tft.text(small_font,"Check hostname on ui",15,38,st7789.WHITE,st7789.BLACK)
            self._tft.text(small_font,"http://" + self.ip,15,56,st7789.WHITE,st7789.BLACK)
        
    def _write_option(self, index, color, back):
        self._tft.text(
            font,
            self._display_options[index].display,
            234 - (len(self._display_options[index].display) * 16),
            12 + (index * 60),
            color,
            back)

    def _menu_button_handler(self, index):
        if index >= len(self._display_options) or self._info:
            return
        self.disable_buttons() 
        self._write_option(index, st7789.BLACK, st7789.WHITE)
        # debounce time - we ignore any activity diring this period 
        
        self._gbs_api.set_option(self._display_options[index].id)
        utime.sleep_ms(600)
        self._write_option(index, st7789.WHITE, st7789.BLACK)
        self.enable_buttons()
        
    def previous_page(self):
        self.set_page(self._page - 1)
        
    def next_page(self):
        self.set_page(self._page + 1)
        
    def set_page(self, page):
        startIndex = page * 4
        display_options = self._options[startIndex: startIndex + 4]
        if(len(display_options) == 0):
            return
        self._display_options = display_options
        self._page = page
        self._tft.fill(st7789.BLACK)
        for opt, x in enumerate(self._display_options):
            self._write_option(opt, st7789.WHITE, st7789.BLACK)
            
    def toogle_info(self):
        self._info= not self._info
        if self._info:
            self._tft.fill(st7789.BLACK)
            self._tft.text(small_font,"GBS: " + self._gbs_api.get_url(),15,20,st7789.WHITE,st7789.BLACK)
            self._tft.text(small_font,"GUI: http://" + self.ip,15,45,st7789.WHITE,st7789.BLACK)
        else:
            self.set_page(self._page)
            
    def clear(self):
        self.loading_increment = 10
        self._tft.fill(st7789.BLACK)
        
    def write(self, text, x, y, font=small_font, color=st7789.WHITE):
        self._tft.text(font,text,x,y,color,st7789.BLACK)
        
    def loadingIncrement(self):
        self._tft.text(font,".",self.loading_increment,200,st7789.WHITE,st7789.BLACK)
        self.loading_increment = self.loading_increment + 40
        if(self.loading_increment > 240):
            self.loading_increment = 10
            self._tft.fill_rect(0, 200, 240, 40, st7789.BLACK)
        
        
