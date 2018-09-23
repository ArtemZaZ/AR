import OpenGL.GL as gl
import numpy as np

# TODO: в процессе дополнить

""" Перевод типов из OpenGL в numpy """
variable_G_to_N = {
    gl.GL_FLOAT: np.float32,
    gl.GL_DOUBLE: np.float64,
    gl.GL_INT: np.int32,
    gl.GL_UNSIGNED_INT64: np.uint64,
    gl.GL_UNSIGNED_INT: np.uint32
}

""" Перевод типов из numpy в OpenGL """
variable_N_to_G = {
    np.dtype(np.float32): gl.GL_FLOAT,
    np.dtype(np.float64): gl.GL_DOUBLE,
    np.dtype(np.int32): gl.GL_INT,
    np.dtype(np.uint32): gl.GL_UNSIGNED_INT,
}

""" Доступные типы для Variable """
variableTypes = [gl.GL_FLOAT, gl.GL_DOUBLE, gl.GL_BYTE,
                 gl.GL_UNSIGNED_BYTE, gl.GL_SHORT,
                 gl.GL_UNSIGNED_SHORT, gl.GL_UNSIGNED_INT,
                 gl.GL_UNSIGNED_INT64, gl.GL_CHAR,
                 gl.GL_INT, gl.GL_BOOL,
                 gl.GL_HALF_NV, gl.GL_VOID_P,
                 gl.GL_FLOAT_VEC2, gl.GL_FLOAT_VEC3,
                 gl.GL_FLOAT_VEC4,
                 gl.GL_FLOAT_MAT2, gl.GL_FLOAT_MAT3,
                 gl.GL_FLOAT_MAT4,
                 gl.GL_SAMPLER_1D, gl.GL_SAMPLER_2D,
                 gl.GL_SAMPLER_CUBE, gl.GL_DOUBLE_VEC2,
                 gl.GL_DOUBLE_VEC3, gl.GL_DOUBLE_VEC4,
                 gl.GL_DOUBLE_MAT2, gl.GL_DOUBLE_MAT3,
                 gl.GL_DOUBLE_MAT4, gl.GL_INT_VEC2,
                 gl.GL_INT_VEC3, gl.GL_INT_VEC4]

uniformTypesToFunctions = {
    gl.GL_FLOAT: (gl.glUniform1fv, 1, False),
    gl.GL_DOUBLE: (gl.glUniform1dv, 1, False),
    gl.GL_INT: (gl.glUniform1iv, 1, False),
    gl.GL_BOOL: (gl.glUniform1iv, 1, False),
    gl.GL_FLOAT_VEC2: (gl.glUniform2fv, 2, False),
    gl.GL_FLOAT_VEC3: (gl.glUniform3fv, 3, False),
    gl.GL_FLOAT_VEC4: (gl.glUniform4fv, 4, False),
    gl.GL_FLOAT_MAT2: (gl.glUniformMatrix2fv, 1, True),
    gl.GL_FLOAT_MAT3: (gl.glUniformMatrix3fv, 1, True),
    gl.GL_FLOAT_MAT4: (gl.glUniformMatrix4fv, 1, True),
    gl.GL_DOUBLE_VEC2: (gl.glUniform2dv, 2, False),
    gl.GL_DOUBLE_VEC3: (gl.glUniform3dv, 3, False),
    gl.GL_DOUBLE_VEC4: (gl.glUniform4dv, 4, False),
    gl.GL_DOUBLE_MAT2: (gl.glUniformMatrix2dv, 1, True),
    gl.GL_DOUBLE_MAT3: (gl.glUniformMatrix3dv, 1, True),
    gl.GL_DOUBLE_MAT4: (gl.glUniformMatrix4dv, 1, True),
    gl.GL_INT_VEC2: (gl.glUniform2iv, 2, False),
    gl.GL_INT_VEC3: (gl.glUniform3iv, 3, False),
    gl.GL_INT_VEC4: (gl.glUniform4iv, 4, False),
    gl.GL_SAMPLER_1D: (gl.glUniform1i, 1, False),
    gl.GL_SAMPLER_2D: (gl.glUniform1i, 1, False),
    gl.GL_SAMPLER_CUBE: (gl.glUniform1i, 1, False)
}
