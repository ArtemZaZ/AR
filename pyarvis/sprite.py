from vispy.gloo import VertexBuffer
from vispy.scene import Widget
from vispy.visuals import Visual
import numpy as np

VERTEX_SHADER = """
    attribute vec2 position;
    attribute vec2 texCoord;
    varying vec2 v_texCoord;
    uniform float depth;
    void main()
    {
        gl_Position = $transform(vec4(position, depth, 1.0));
        v_texCoord = texCoord;
    }
"""

FRAGMENT_SHADER = """
    uniform sampler2D texture;
    varying vec2 v_texCoord;
    void main()
    {
        gl_FragColor = texture2D(texture, v_texCoord);
    }
"""


class Sprite(Widget):
    def __init__(self, data, **kwargs):
        self._visual = SpriteVisual(data, **kwargs)
        Widget.__init__(self, **kwargs)
        self.add_subvisual(self._visual)

    @property
    def rect(self):
        return self._visual.rect

    @rect.setter
    def rect(self, value):
        self._visual.rect = value

    @property
    def data(self):
        return self._visual.data

    @data.setter
    def data(self, value):
        self._visual.data = value

    @property
    def depth(self):
        return self._visual.depth

    @depth.setter
    def depth(self, value):
        self._visual.depth = value


class SpriteVisual(Visual):
    def __init__(self, data, rect=(0, 0, 1, 1), depth=0.0, **kwargs):
        self._data = data
        self._depth = depth
        vertices = np.array([(-1, -1), (-1, +1), (+1, -1), (+1, +1)],
                            dtype=np.float32)
        r = self._rect = rect
        texCoord = np.array([(r[0], r[1]), (r[0], r[1] + r[3]), (r[0] + r[2], r[1]), (r[0] + r[2], r[1] + r[3])],
                            dtype=np.float32)

        self._texNeedUpdate = False
        self._texCoordNeedUpdate = False
        self._depthNeedUpdate = False

        Visual.__init__(self, VERTEX_SHADER, FRAGMENT_SHADER)
        self.shared_program["position"] = VertexBuffer(vertices)
        self.shared_program["texCoord"] = VertexBuffer(texCoord)
        self.shared_program['depth'] = self._depth
        self.shared_program['texture'] = self._data
        self.set_gl_state(blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))
        self._draw_mode = 'triangle_strip'

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value
        self._texCoordNeedUpdate = True

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._texNeedUpdate = True

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depthNeedUpdate = True
        self._depth = value

    def _prepare_transforms(self, view):
        view.view_program.vert['transform'] = view.transforms.get_transform()

    def _prepare_draw(self, view):
        if self._texNeedUpdate:
            self.shared_program['texture'] = self._data
            self._texCoordNeedUpdate = False
        if self._texCoordNeedUpdate:
            r = self._rect
            self.shared_program['texCoord'] = np.array([(r[0], r[1]), (r[0], r[1] + r[3]), (r[0] + r[2], r[1]),
                                                        (r[0] + r[2], r[1] + r[3])], dtype=np.float32)
            self._texCoordNeedUpdate = False
        if self._depthNeedUpdate:
            self.shared_program['depth'] = self._depth
            self._depthNeedUpdate = False

