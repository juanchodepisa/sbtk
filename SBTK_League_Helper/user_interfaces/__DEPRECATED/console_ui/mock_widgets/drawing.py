from math import floor

from src import class_initializer
from src.tools.markers import AdHocMarker

# ┌─┬┐ 
# │ ││ 
# ├─┼┤ 
# └─┴┘ 
# ("simple border", "CP850")
# ╔═╦╗
# ║ ║║
# ╠═╬╣
# ╚═╩╝
# ("double border", "CP850")
# +-++  
# | ||  NOT YET SUPPORTED
# +-++
# +-++
     # .   ,.
# \   / \ /  \  /
 # \ /   X    )(   or whatever
  # V   / \  /  \
         # \/


@class_initializer
class BoxDrawingOperations:
    borders_simple = "┌─┬┐│├┼┤└┴┘"
    borders_double = "╔═╦╗║╠╬╣╚╩╝"
    borders_all    = "┌─┬┐│├┼┤└┴┘╔═╦╗║╠╬╣╚╩╝"
    borders_north  = "│├┼┤└┴┘║╠╬╣╚╩╝"
    borders_south  = "┌┬┐│├┼┤╔╦╗║╠╬╣"
    borders_east   = "┌─┬├┼└┴╔═╦╠╬╚╩"
    borders_west   = "─┬┐┼┤┴┘═╦╗╬╣╩╝"
    
    __border_multipliers = {
        "north" : 0b1011,
        "south" : 0b0111,
        "east" : 0b1110,
        "west" : 0b1101}
        
    __border_numbers_table = tuple({'simple': " ", 'double': " "} for i in range(16))
    
    @classmethod
    def __border_to_binary (Class, char):
        result = 0
        result += (char in Class.borders_north) * 8
        result += (char in Class.borders_south) * 4
        result += (char in Class.borders_east) * 2
        result += (char in Class.borders_west) * 1
        return result
    
    @classmethod
    def __binary_to_border (Class, n, type):
        return Class.__border_numbers_table[n][type]
    
    @classmethod
    def border_type(Class, char):
        if char in Class.borders_simple:
            return "simple"
        elif char in Class.borders_double:
            return "double"
        else:
            return None
    
    @classmethod
    def mix_borders(Class, below, above, solid = False, mix_types = False): #solid must be north, south, east, west or False
        typea = Class.border_type(above)
        if typea:
            typeb = Class.border_type(below)
            if (typeb and mix_types) or typea == typeb:
                below = Class.__border_to_binary(below)
                above = Class.__border_to_binary(above)
                if solid:
                    below = below & Class.__border_multipliers[solid]
                return Class.__binary_to_border(above | below, typea)
            else:
                return above
        else:
            return above
    
    
    @classmethod
    def __initClass__(Class):
        for char in Class.borders_simple:
            i = Class.__border_to_binary(char)
            Class.__border_numbers_table[i]['simple'] = char
            
        for char in Class.borders_double:
            i = Class.__border_to_binary(char)
            Class.__border_numbers_table[i]['double'] = char


            

##############################################################################################
# THE FOLLOWING TWO CLASSES IMPLEMENT A PIXMAP

# Every pixel is a character,
# characters should be limited to CODE PAGE 850 so that they are supported by CMD

##############################################################################################

class BufferedLine_CP850(list): 
    def __init__(self, len, parent, line_number):
        self.__len
        self.__parent = parent
        self.__line_number = line_number
        self.__pending_change = True
        super(BufferedLine_CP850, self).__init__([" "]*len)
    
    def flush(self): # Always flush changes, once all changes are done
        if self.__pending_change:
            self.__string = "".join(self)
            self.__pending_change = False
    
    def resize (self, len):
        if len != self.__len:
            self.__pending_change = True
            while len < self.__len:
                self.pop()
                self.__len -= 1
            while len > self._len:
                self.append(" ")
                self.__len += 1
                
    def __setitem__(*args, **kwargs):
        self = args[0]
        args = args[1:]
        super(BufferedLine_CP850, self).__setitem___(*args,**kwargs)
        self.__pending_change = True
        self.__parent.signal_pending_change()
    
    def draw (self, string, offset = 0, limit = float("inf"), repetitions = 1):
        limit = min (limit, self.__len)
        if limit <= offset or repetitions <= 0:
            pass
        else:
            l =  len(string)
            if repetitions < 1:
                l = floor (l * repetitions)
            end = offset + l
            end = min(end, limit)
            l = end - offset
            self [offset:end] = list(string[:l])
            self.draw (string, offset = end, limit = limit, repetitions = repetitions-1)
    
    def draw_mix_border(self, bfline, offset = 0, mix_types = True):
        if len(bfline) == 1:
            self.superpose_bd_pixel(end-1, bfline[l-1], False, mix_types)
        elif bfline.is_first():
            if bfline.is_last():
                self.__draw_mix_borderline (bfline, offset, False, mix_types)
            else:
                self.__draw_mix_borderline (bfline, offset, 'north', mix_types)
        elif bfline.is_last():
            self.__draw_mix_borderline (bfline, offset, 'south', mix_types)
        else:
            l = len(bfline)
            end = offset + l
            self.superpose_bd_pixel(end-1, bfline[l-1], 'east', mix_types)
            self.superpose_bd_pixel(offset, bfline[0], 'west', mix_types)
            self [offset+1 : end-1] = bfline[1 : l-2]
            
    
    def __draw_mix_borderline (self, bfline, offset, orientation, mix_types):
        l = len(bfline)
        end = offset + l
        self.superpose_bd_pixel(end-1, bfline[l-1], False, mix_types)
        self.superpose_bd_pixel(offset, bfline[0], False, mix_types)
        for i in range (1, end-1):
            self.superpose_bd_pixel(offset+i, bfline[i], orientation, mix_types)
    
    
    def superpose_bd_pixel(self, postition, pixel, orientation, mix_types): #bd for Box Drawing
        self[position] = BoxDrawingOperations.mix_borders(self[position], pixel, solid = orientation, mix_types = mix_types)
    
    def is_first(self):
        return self.__line_number == 0
    def is_last(self):
        return self.__line_number + 1 == len (self.__parent)
        
        
    def __len__(self):
        return self.__len
    def __str__(self):
        while self.__pending_change:
            self.flush()
        return self.__string


class BufferedMatrix_CP850(list):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        lines = [BufferedLine_CP850(width, self, row) for row in range(height)]
        super(BufferedMatrix_CP850, self).__init__(lines)
        self.__pending_change = True
        
    def signal_pending_change(self):
        self.__pending_change = True
    
    def flush(self):
        if self.__pending_change:
            self.__string = "".join(str(line).join("\n") for line in self)
            self.__pending_change = False
        
    
    def resize (self, width, height):
        if witdh != self.__width:
            self.__pending_change = True
            for line in self:
                line.resize(width)
        if height != self.__height:
            self.__pending_change = True
            while height < self.__height:
                self.pop()
                self.__height -= 1
            while height > self._height:
                self.append(BufferedLine_CP850(width, self, self.height))
                self.__height += 1
    
    def draw_mix_border (self, bfmatrix, offset_x = 0, offset_y = 0, mix_types = True):
        w = bfmatrix.width()
        h = bfmatrix.height()
        end_x = offset_x + w
        end_y = offset_y + h
        max_w = max(end_x, self.__width)
        max_h = max(end_y, self.__height)
        self.resize (max_w, max_h)
        
        for j in range (h):
            self[offset_y+j].draw_mix_border(bfmatrix[j], offset = offset_x, mix_types = mix_types)
        
    
    
    
    def __len__(self):
        return self.__width
    def width(self):
        return self.__width
    def height(self):
        return self.__height
    def __str__(self):
        while self.__pending_change:
            self.flush()
        return self.__string

        
        
        
        
        
"""

THE FOLLOWING ARE INCOMPLETE

These classes deal with parsing text, to be passed into
pixmaps, etc.




"""

ret_mark = AdHocMarker('return', str)
pgf_mark = AdHocMarker('paragraph', str)
spw_mark = AdHocMarker('split word', str)
inl_mark = AdHocMarker('inline break', str)
eot_mark = AdHocMarker('end of text', str)

def is_return(mark):
    return mark is ret_mark or mark is pgf_mark

 
class BufferedListString(list):                        # Intended for use as a list of characters
    def __init__(self, string = "", breakmark = None): # String can be any iterable of characters
        super(BufferedListString, self).__init__(string)
        self.breakmark = breakmark
        self.flush()
        
    def flush(self): # Always flush changes, once all changes are done
        self.__string = "".join(self)
    
    def breakline (self, n, break_words = False): # searches only spaces, not tabs or any other character
        class MyException(Exception):
            pass
        def seek_space(min, max):
            while min <= max:
                if self[max] == ' ':
                    break
                else:
                    max -= 1
            else:
                raise MyException()
            return max
        
        Class = type(self)
        l = len(self)
        breaktype = spw_mark
        last_break = 0
        processed_characters = 0
        this_break = n
        result = []
        
        while this_break < l:
            if break_words:
                processed_characters = this_break
            else:
                try:
                    this_break = seek_space(last_break, this_break)
                    breaktype = inl_mark
                    processed_characters = this_break + 1 #includes the space itself, which is dumped
                except MyException:
                    processed_characters = this_break
            
            result.append(Class(self[last_break:this_break], breakmark = breaktype))
            breaktype = spw_mark
            last_break = processed_characters
            this_break = last_break + n
        else:
            new_self = self[last_break:]
            self.clear()
            self.extend(new_self)
            self.flush()
            result.append(self)
        
        return result
        
    def __repr__(self):
        return self.__string
    def __str__(self):
        return self.__string
    

class BufferedLinedText(list): # Intended for use as a list of buffered list strings
    # MISSING: A FLUSH METHOD

    def __init__(self, text = "", maxlen = float('inf'), break_words = False):
        blocks = text.split('\n')
        breaktype = eot_mark
        for i in range(len(blocks)-1,-1,-1):
            string = blocks[i]
            blocks[i] = BufferedListString(string, breakmark = breaktype)
            if string:
                breaktype = ret_mark
            else:
                breaktype = pgf_mark
        
        lines = [x for block in blocks for x in block.breakline(maxlen, break_words = break_words)]
        super(BufferedLinedText, self).__init__(lines)
        self.__len = max([len(x) for x in lines])
        self.__height = len(lines)
        self.__string = ""
        for line in lines:
            self.__string += str(line)+"\n"
        
    
    def __len__(self):
        return self.__len
    def width(self):
        return self.__len
    def height(self):
        return self.__height
    def __str__(self):
        return self.__string