import numpy as np
import OpenGL.GL as gl
from OpenGL.GL import shaders
from glEngine.arrays import VertexArray
from glEngine.buffers import VertexBuffer, IndexBuffer
import warnings


class Mesh:
    """
    Класс меша, принимает вершинный и фрагментный шейдер + kwargs с ключом - именем аттрибута,
    значением - данными аттрибута
    vertices = (name, data)
    """
    # TODO: придумать и переделать так, чтобы не нужно было вводить vertices
    def __init__(self, vertexShader, fragmentShader, vertices, faces, **kwargs):
        self._vertexShaderSource = vertexShader
        self._fragmentShaderSource = fragmentShader
        self._programAttributeList = []  # список аттрибутов шейдерной программы
        self._verticesName = vertices[0]
        self._vertices = vertices[1]
        self.__setattr__(self._verticesName, self._vertices)  # добавляем аттрибут вершин
        self.faces = faces
        for key, value in kwargs.items():  # добавляем все аттрибуты
            self.__setattr__(key, value)
            self._programAttributeList.append(key)
        self._vao = None
        self._vertexBuffer = None
        self._indexBuffer = None

        self._program = shaders.compileProgram(
            shaders.compileShader(self._vertexShaderSource, gl.GL_VERTEX_SHADER),
            shaders.compileShader(self._fragmentShaderSource, gl.GL_FRAGMENT_SHADER)
        )

    def create(self):
        numpyList = [(self._verticesName, self._vertices.dtype, self._vertices.shape[1])]   # создаем список, который
        #  запихаем в numpy
        for key in self._programAttributeList:  # проходимся по каждому аттрибуту шейдерной программы
            value = self.__getattribute__(key)
            numpyList.append((key, value.dtype, value.shape[1]))    # добавляем кортеж в список
        gl.glUseProgram(self._program)
        self._vao = VertexArray()
        self._vertexBuffer = np.zeros(self._vertices.shape[0], numpyList).view(VertexBuffer)    # создаем буффер вершин
        self._vertexBuffer.__init__(self._program)

        """ Записываем данные в вершинный буффер """
        self._vertexBuffer[self._verticesName][...] = self._vertices
        for key in self._programAttributeList:
            self._vertexBuffer[key][...] = self.__getattribute__(key)

        """ индексный буффер """
        if (self.faces.dtype is np.dtype(np.uint64)) or (self.faces.dtype is np.dtype(np.int64)):
            warnings.warn("integer 64bit dtype not supported, dtype is translated to uint32")
            self._indexBuffer = np.zeros(self.faces.shape, dtype=np.uint32).view(IndexBuffer)
        else:
            self._indexBuffer = np.zeros(self.faces.shape, dtype=self.faces.dtype).view(IndexBuffer)

        self._indexBuffer.__init__()
        self._indexBuffer[...] = self.faces

        """ связываем все """
        self._vao.vbo = self._vertexBuffer
        self._vao.ibo = self._indexBuffer
        self._vao.create()
        gl.glUseProgram(0)

    @property
    def program(self):
        return self._program

    def draw(self, mode=gl.GL_TRIANGLE_STRIP):
        gl.glUseProgram(self._program)
        self._vao.draw(mode=mode)
        gl.glUseProgram(0)


if __name__ == "__main__":
    a = np.array([[1, 2, 3], [4, 5, 6]])
    Mesh(None, None, ("position", a), None).create()
