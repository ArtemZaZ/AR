import OpenGL.GL as gl
import numpy as np

variable_G_to_N = {
    gl.GL_FLOAT: np.float32,
    gl.GL_DOUBLE: np.float64,
    gl.GL_INT: np.int32,
    gl.GL_UNSIGNED_INT64: np.uint64,
    gl.GL_UNSIGNED_INT: np.uint32
}

variable_N_to_G = {
    np.dtype(np.float32): gl.GL_FLOAT,
    np.dtype(np.float64): gl.GL_DOUBLE,
    np.dtype(np.int32): gl.GL_INT,
    np.dtype(np.uint64): gl.GL_UNSIGNED_INT64,
    np.dtype(np.uint32): gl.GL_UNSIGNED_INT
}
