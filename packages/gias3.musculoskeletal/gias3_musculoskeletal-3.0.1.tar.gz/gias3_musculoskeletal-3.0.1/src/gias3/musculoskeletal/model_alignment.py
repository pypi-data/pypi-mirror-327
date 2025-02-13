"""
FILE: model_alignment.py
LAST MODIFIED: 24-12-2015 
DESCRIPTION: functions for alignining fieldwork models of individual bones

===============================================================================
This file is part of GIAS3. (https://github.com/musculoskeletal/gias3)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
===============================================================================
"""

import copy
import logging

import numpy
from scipy.optimize import fmin

from gias3.common import geoprimitives
from gias3.common import transform3D
from gias3.learning import PCA_fitting
from gias3.musculoskeletal import fw_femur_measurements
from gias3.musculoskeletal import fw_femur_model_data as fmd
from gias3.musculoskeletal import fw_model_landmarks
from gias3.registration import alignment_analytic
from gias3.registration import alignment_fitting

log = logging.getLogger(__name__)


def normaliseVector(v):
    return v / numpy.linalg.norm(v)


def _makeLandmarkObj(targ, evaluator):
    def obj(P):
        # print targ
        return ((targ - evaluator(P)) ** 2.0).sum()

    return obj


# =======================================================#
# general alignment                                     #
# =======================================================#
def alignMeshParametersRigid(g_fields, target_gf=None, ret_transforms=False):
    # procrustes alignment of gFields to the 1st gField

    # evaluate points from each g
    # d = 5
    # X = [ g.evaluate_geometric_field( d ).T for g in gFields ]
    XNodes = [g.get_all_point_positions() for g in g_fields]

    if target_gf is None:
        # use the first one
        target_gf = g_fields[0]

    # targ = targetGF.evaluate_geometric_field( d ).T
    targNodes = target_gf.get_all_point_positions()
    targetCoM = target_gf.calc_CoM()

    # rigid fit each to X[targI] 
    alignedParams = []
    Ts = []
    for i in range(len(g_fields)):
        CoMTrans = targetCoM - g_fields[i].calc_CoM()
        x0 = numpy.hstack([CoMTrans, 0, 0, 0])
        # fit nodes
        tOpt = alignment_fitting.fitRigid(XNodes[i], targNodes, xtol=1e-6, verbose=1)[0]
        # fit surface data
        # tOpt = alignment_fitting.fitRigid( X[i], targ, xtol=1e-5, verbose=1 )[0]

        # apply transform to gfield parameters
        gFieldNodes = g_fields[i].get_field_parameters().squeeze().T
        alignedParams.append(transform3D.transformRigid3DAboutCoM(gFieldNodes, tOpt).T[:, :, numpy.newaxis])
        Ts.append(tOpt)

    if ret_transforms:
        return alignedParams, Ts
    else:
        return alignedParams


def alignMeshParametersProcrustes(g_fields, target_gf=None, ret_transforms=False):
    # procrustes alignment of gFields to the 1st gField

    # evaluate points from each g
    # d = 5
    # X = [ g.evaluate_geometric_field( d ).T for g in gFields ]
    XNodes = [g.get_all_point_positions() for g in g_fields]

    if target_gf is None:
        # use the first one
        target_gf = g_fields[0]

    # targ = targetGF.evaluate_geometric_field( d ).T
    targNodes = target_gf.get_all_point_positions()

    # rigid fit each to X[targI] 
    sizes = []
    alignedParams = []
    Ts = []
    for i in range(len(g_fields)):
        # fit nodes
        tOpt = alignment_fitting.fitRigidScale(XNodes[i], targNodes, xtol=1e-3, verbose=1)[0]
        # fit surface data
        # tOpt = alignment_fitting.fitRigidScale( X[i], targ, xtol=1e-5 )[0]

        # apply transform to gfield parameters
        gFieldNodes = g_fields[i].get_field_parameters().squeeze().T
        alignedParams.append(transform3D.transformRigidScale3DAboutCoM(gFieldNodes, tOpt).T[:, :, numpy.newaxis])
        sizes.append(tOpt[-1])
        Ts.append(tOpt)

    if ret_transforms:
        return alignedParams, numpy.array(sizes), Ts
    else:
        return alignedParams, numpy.array(sizes)


def alignModelLandmarksLinScale(gf, landmarks, weights=1.0,
                                gf_params_callback=None, fminargs=None):
    """
    Rigid transformation plus scaling to register a fieldwork model to its
    landmarks. Registration is performed in two stages: rigid-body, then
    rigid-body plus isotropic scaling.

    Inputs
    ------
    gf : geometric_field instance
        The model to be registered
    landmarks : list of 2-tuples
        A list of tuples [(landmark name, landmark coords),...]
    weights : float or list of floats [optional]
        The weighting for each landmark. If a float, then all landmarks will
        have the same weighting.
    GFParamsCallback : function [optional]
        If defined, function is called after each registration stage with
    fminargs : dict [optional]
        A dictionary of keyword arguments for numpy.optimize.fmin.

    Returns
    -------
    sourceGF : geometric_field instance
        The registered model
    SSE : tuple
        The sum of squared errors from each stage of the registration
    xOpt2 : 1-d array
        The optimal transform vector
    """

    if fminargs is None:
        fminargs = {'maxfun': 100000}

    sourceGF = copy.deepcopy(gf)
    CoM0 = sourceGF.calc_CoM()
    p0 = sourceGF.get_field_parameters()[:, :, 0].T
    targetLandmarks = []
    ldObjs = []
    for ldName, ldTarg in landmarks:
        targetLandmarks.append(ldTarg)
        evaluator = fw_model_landmarks.make_landmark_evaluator(
            ldName, sourceGF
        )
        ldObjs.append(_makeLandmarkObj(ldTarg, evaluator))

    # rigid reg obj
    def obj1(x):
        pT = transform3D.transformRigid3DAboutP(
            p0, x, CoM0
        ).T
        se = numpy.array([f(pT) for f in ldObjs])
        sse = (se * weights).sum()
        return sse

    # rigid + iso scale reg obj
    def obj2(x):
        pT = transform3D.transformRigidScale3DAboutP(
            p0, x, CoM0
        ).T
        se = numpy.array([f(pT) for f in ldObjs])
        sse = (se * weights).sum()
        return sse

    P0 = gf.get_field_parameters()
    n0 = ldObjs[0](P0)
    x01 = numpy.hstack([targetLandmarks[0] - n0, 0, 0, 0])

    # rigid reg
    xOpt1 = fmin(obj1, x01, **fminargs)
    sse1 = obj1(xOpt1)
    pT = transform3D.transformRigid3DAboutP(
        p0, xOpt1, CoM0
    ).T[:, :, numpy.newaxis]
    if gf_params_callback is not None:
        gf_params_callback(pT)
    # rigid + isotropic scale
    x02 = numpy.hstack([xOpt1, 1.0])
    xOpt2 = fmin(obj2, x02, **fminargs)
    sse2 = obj2(xOpt2)
    pT = transform3D.transformRigidScale3DAboutP(
        p0, xOpt2, CoM0
    ).T[:, :, numpy.newaxis]
    if gf_params_callback is not None:
        gf_params_callback(pT)
    # rigid + orthogonal scale
    # not implemented

    sourceGF.transformRigidScaleRotateAboutP(xOpt2, CoM0)

    return sourceGF, (sse1, sse2), xOpt2


def alignModelLandmarksPC(gf, landmarks, pc, pcs, weights=1.0,
                          gf_params_callback=None, mw0=1.0, mwn=1.0, fminargs=None,
                          ):
    """
    Principal components-based non-linear scaling to register a fieldwork
    model to its landmarks. Registration is performed in three stages:
    rigid-body, then rigid-body plus first pc, then rigid-body with all
    defined pcs.

    Inputs
    ------
    gf : geometric_field instance
        The model to be registered
    pc : PrincipalComponent instance
        The principal components to deform the model along
    landmarks : list of 2-tuples
        A list of tuples [(landmark name, landmark coords),...]
    pcs : int
        The number of principal components numbers to use in the registration.
    weights : float or list of floats [optional]
        The weighting for each landmark. If a float, then all landmarks will
        have the same weighting.
    GFParamsCallback : function [optional]
        If defined, function is called after each registration stage with
        the optimal model parameters.
    mw0 : float [optional]
        Mahalanobis distance penalty weight for the rigid + 1st pc stage
    mwn : float [optional]
        Mahalanobis distance penalty weight for the rigid + all pcs stage
    fminargs : dict [optional]
        A dictionary of keyword arguments for numpy.optimize.fmin.

    Returns
    -------
    sourceGF : geometric_field instance
        The registered model
    SSE : tuple
        The sum of squared errors from each stage of the registration
    rigidModeNT : 1-d array
        The optimal transform vector
    """
    sourceGF = copy.deepcopy(gf)
    targetLandmarks = []
    ldObjs = []
    for ldName, ldTarg in landmarks:
        targetLandmarks.append(ldTarg)
        evaluator = fw_model_landmarks.make_landmark_evaluator(ldName, sourceGF)
        ldObjs.append(_makeLandmarkObj(ldTarg, evaluator))

    def obj(P):
        P3 = P.reshape((3, -1))
        se = numpy.array([f(P3) for f in ldObjs])
        # print se
        sse = (se * weights).sum()
        return sse

    pcFitter = PCA_fitting.PCFit(pc=pc)
    pcFitter.useFMin = True
    if fminargs is not None:
        if 'xtol' in fminargs:
            pcFitter.xtol = fminargs['xtol']
        if 'ftol' in fminargs:
            pcFitter.ftol = fminargs['ftol']
        if 'maxiter' in fminargs:
            pcFitter.maxiter = fminargs['maxiter']
        if 'maxfev' in fminargs:
            pcFitter.maxfev = fminargs['maxfev']
    else:
        pcFitter.maxfev = 100000

    P0 = pc.getMean().reshape((3, -1))
    n0 = ldObjs[0](P0)
    x0 = numpy.hstack([targetLandmarks[0] - n0, 0, 0, 0])

    # targetCoM = (targetHC + ((targetMEC+targetLEC)/2.0))/2.0
    # x0 = numpy.hstack([targetCoM - sourceGF.calc_CoM(), 0, 0, 0])

    rigidT, rigidP = pcFitter.rigidFit(obj, x0=x0)
    sourceGF.set_field_parameters(rigidP.reshape((3, -1, 1)))
    rigidSSE = obj(rigidP)
    if gf_params_callback is not None:
        gf_params_callback(rigidP)

    rigidMode0T, rigidMode0P = pcFitter.rigidMode0Fit(obj, mWeight=mw0)
    sourceGF.set_field_parameters(rigidMode0P.reshape((3, -1, 1)))
    rigidMode0SSE = obj(rigidMode0P)
    if gf_params_callback is not None:
        gf_params_callback(rigidMode0P)

    rigidModeNT, rigidModeNP = pcFitter.rigidModeNFit(
        obj, modes=list(range(1, pcs)), mWeight=mwn
    )
    sourceGF.set_field_parameters(rigidModeNP.reshape((3, -1, 1)))
    rigidModeNSSE = obj(rigidModeNP)
    if gf_params_callback is not None:
        gf_params_callback(rigidModeNP)

    return sourceGF, (rigidSSE, rigidMode0SSE, rigidModeNSSE), rigidModeNT


# =======================================================#
# femur alignment                                       #
# =======================================================#
def createFemurACS(head, mc, lc):
    o = (mc + lc) / 2.0
    z = normaliseVector(head - o)
    y = normaliseVector(numpy.cross(z, (o - lc)))
    x = normaliseVector(numpy.cross(y, z))
    u = numpy.array([o, o + x, o + y, o + z])
    return u


def createFemurACSISB(head, mc, lc, side='left'):
    """Axes: x-anterior, y-superior, z-right
    origin: midpoint of epicondyles
    """
    #  origin - midpoint of epicondyles
    o = (mc + lc) / 2.0
    # y - origin to head
    y = normaliseVector(head - o)
    # z - right in plane of head, mc, lc
    n1 = normaliseVector(numpy.cross(mc - head, lc - head))
    z = normaliseVector(numpy.cross(n1, y))
    if side == 'right':
        z *= -1.0
    # x - anteriorly 
    x = normaliseVector(numpy.cross(y, z))
    return o, x, y, z


def createFemurACSOpenSim(head, mc, lc, side='left'):
    """Axes: x-anterior, y-superior, z-right
    origin: femoral head centre
    """
    #  temp origin - midpoint of epicondyles
    o_ = (mc + lc) / 2.0
    # y - origin to head
    y = normaliseVector(head - o_)
    # z - right in plane of head, mc, lc
    n1 = normaliseVector(numpy.cross(mc - head, lc - head))
    z = normaliseVector(numpy.cross(n1, y))
    # if left, z should point towards to MC
    if side == 'left':
        if numpy.dot(z, mc - o_) < 0.0:
            z *= -1.0

    # if right, z should point towards LC
    elif side == 'right':
        if numpy.dot(z, lc - o_) < 0.0:
            z *= -1.0
    else:
        raise ValueError('Invalid side value {}'.format(side))

    # x - anteriorly 
    x = normaliseVector(numpy.cross(y, z))
    return head, x, y, z


def alignAnatomicFemur(X, head, mc, lc, return_t=False):
    """ aligns points X, with head CoM, mc CoM, lc CoM, to the origin
    and global axes (femur only). Grood and Suntay 1983 system.
    """

    o = (mc + lc) / 2.0
    z = normaliseVector(head - o)
    y = normaliseVector(numpy.cross(z, (o - lc)))
    x = normaliseVector(numpy.cross(y, z))

    # o = X.mean(0)

    u = numpy.array([o, o + x, o + y, o + z])

    ut = numpy.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    t = transform3D.directAffine(u, ut)
    if t.shape == (3, 4):
        t = numpy.vstack([t, [0, 0, 0, 1]])

    if return_t:
        return transform3D.transformAffine(X, t), t
    else:
        return transform3D.transformAffine(X, t)


femurLandmarkNodes = {
    'MEC': 633,
    'LEC': 546,
    'FGT': 172,
}


def alignFemurLandmarksRigidScale(gf, landmarks, t0=None, r0=None, s0=None):
    """
    landmarks: a list of tuples [(landmark name, landmark coords),...]
    valid landmark names: FHC, MEC, LEC

    """
    targetLandmarks = []
    sourceLandmarks = []
    for ldName, ldTarg in landmarks:
        if ldName == 'FHC':
            ldName = 'HC'
        evaluator = fw_model_landmarks.make_landmark_evaluator('femur-' + ldName, gf)
        sourceLandmarks.append(evaluator(gf.get_field_parameters()))
        targetLandmarks.append(ldTarg)

    targetLandmarks = numpy.array(targetLandmarks)
    sourceLandmarks = numpy.array(sourceLandmarks)
    T0 = numpy.zeros(7)
    if s0 is None:
        T0[6] = 1.0
    else:
        T0[6] = s0

    if t0 is None:
        T0[:3] = targetLandmarks.mean(0) - sourceLandmarks.mean(0)
    else:
        T0[:3] = t0[:]

    if r0 is not None:
        T0[3:6] = r0[:]

    TOpt, fittedLandmarks, (rms0, rmsOpt) = alignment_fitting.fitRigidScale(
        sourceLandmarks,
        targetLandmarks,
        t0=T0,
        xtol=1e-9,
        output_errors=1)

    gf.transformRigidScaleRotateAboutP(TOpt, sourceLandmarks.mean(0))

    return gf, (rms0, rmsOpt), TOpt


def alignFemurLandmarksPC(gf, pc, landmarks, gf_params_callback=None, mw0=1.0, mwn=1.0):
    """
    landmarks: a list of tuples [(landmark name, landmark coords),...]
    valid landmark names: FHC, MEC, LEC

    """
    headElem = 0

    sourceGF = copy.deepcopy(gf)
    headNodes = list(sourceGF.ensemble_field_function.mapper._element_to_ensemble_map[headElem].keys())
    hasFHC = False
    targetFHC = None
    targetLandmarks = []
    landmarkNodes = []
    for ln, lc in landmarks:
        if ln == 'FHC':
            hasFHC = True
            targetFHC = lc
        elif ln in femurLandmarkNodes:
            targetLandmarks.append(lc)
            landmarkNodes.append(femurLandmarkNodes[ln])
        else:
            log.debug('WARNING: landmark %s unsupported')

    if hasFHC:
        targetLandmarks.append(targetFHC)

    def obj(p):
        P = p.reshape((3, -1))
        x = numpy.array([P[:, l] for l in landmarkNodes])
        if hasFHC:
            headC = geoprimitives.fitSphereAnalytic(P[:, headNodes].T)[0]
            x = numpy.vstack([x, headC])
        # e = numpy.sqrt((((x - targetLandmarks)**2.0).sum(1)).mean())
        sse = (((x - targetLandmarks) ** 2.0).sum(1)).sum()
        return sse

    pcFitter = PCA_fitting.PCFit(pc=pc)
    pcFitter.useFMin = True
    pcFitter.ftol = 1e-3

    P0 = pc.getMean().reshape((3, -1))
    n0 = P0[:, landmarkNodes[0]]
    x0 = numpy.hstack([targetLandmarks[0] - n0, 0, 0, 0])

    # targetCoM = (targetHC + ((targetMEC+targetLEC)/2.0))/2.0
    # x0 = numpy.hstack([targetCoM - sourceGF.calc_CoM(), 0, 0, 0])

    rigidT, rigidP = pcFitter.rigidFit(obj, x0=x0)
    sourceGF.set_field_parameters(rigidP.reshape((3, -1, 1)))
    rigidSSE = obj(rigidP)
    if gf_params_callback is not None:
        gf_params_callback(rigidP)

    rigidMode0T, rigidMode0P = pcFitter.rigidMode0Fit(obj, m_weight=mw0)
    sourceGF.set_field_parameters(rigidMode0P.reshape((3, -1, 1)))
    rigidMode0SSE = obj(rigidMode0P)
    if gf_params_callback is not None:
        gf_params_callback(rigidMode0P)

    rigidModeNT, rigidModeNP = pcFitter.rigidModeNFit(obj, modes=[1, 2], m_weight=mwn)
    sourceGF.set_field_parameters(rigidModeNP.reshape((3, -1, 1)))
    rigidModeNSSE = obj(rigidModeNP)
    if gf_params_callback is not None:
        gf_params_callback(rigidModeNP)

    return sourceGF, (rigidSSE, rigidMode0SSE, rigidModeNSSE), rigidModeNT


def alignAnatomicFemurOrthoload(X, head, p1, p2, lcdorsal, mcdorsal, return_t=False):
    """ aligns points X, with head CoM, mc CoM, lc CoM, to the origin
    and global axes (femur only). Grood and Suntay 1983 system.
    """

    o = head
    z = normaliseVector(p1 - p2)
    y = normaliseVector(numpy.cross(z, (lcdorsal - mcdorsal)))
    x = normaliseVector(numpy.cross(y, z))

    # o = X.mean(0)

    u = numpy.array([o, o + x, o + y, o + z])

    ut = numpy.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    t = transform3D.directAffine(u, ut)
    if t.shape == (3, 4):
        t = numpy.vstack([t, [0, 0, 0, 1]])

    if return_t:
        return transform3D.transformAffine(X, t), t
    else:
        return transform3D.transformAffine(X, t)


def alignFemurMeshParametersOrtholoadSingle(femur_model):
    """ given a femur geometric field, align it geometrically.
    returns the aligned field parameters
    """

    # first align to standard ACS
    femurParamsACS, femurACST = alignFemurMeshParametersAnatomicSingle(femur_model)
    femur_model.set_field_parameters(femurParamsACS)
    FM = fw_femur_measurements.FemurMeasurements(femur_model)
    FM.calcMeasurements()

    o = FM.measurements['head_diameter'].centre
    p1 = FM.shaftAxis.a
    p2 = numpy.array([0, 0, 0])

    # condyle dorsal vector
    lcondX = femur_model.evaluate_geometric_field_in_elements([10, 10],
                                                              [fmd.assemblyElementsNumbers['lateralcondyle']]).T
    mcondX = femur_model.evaluate_geometric_field_in_elements([10, 10],
                                                              [fmd.assemblyElementsNumbers['medialcondyle']]).T
    mcDorsal = mcondX[mcondX[:, 1].argmin()]
    lcDorsal = lcondX[lcondX[:, 1].argmin()]

    alignedParams, T = alignAnatomicFemurOrthoload(femur_model.get_field_parameters().squeeze().T,
                                                   o, p1, p2, mcDorsal, lcDorsal, return_t=True)

    alignedParams = alignedParams.T[:, :, numpy.newaxis]
    return alignedParams, T


def alignFemurMeshParametersAnatomicSingle(g):
    """ given a femur geometric field, align it geometrically.
    returns the aligned field parameters
    """
    d = (10, 10)
    head = g.calc_CoM_2D(d, elem=fmd.assemblyElementsNumbers['head'])
    lc = g.calc_CoM_2D(d, elem=fmd.assemblyElementsNumbers['lateralcondyle'])
    mc = g.calc_CoM_2D(d, elem=fmd.assemblyElementsNumbers['medialcondyle'])

    alignedParams, T = alignAnatomicFemur(g.get_field_parameters().squeeze().T, head, mc, lc, return_t=True)
    alignedParams = alignedParams.T[:, :, numpy.newaxis]
    return alignedParams, T


def alignFemurMeshParametersAnatomic(Gs):
    """ given a list of femur geometric fields, align them geometrically.
    returns the aligned field parameters
    """
    alignedParams = []
    d = (10, 10)
    for g in Gs:
        head = g.calc_CoM_2D(d, elem=fmd.assemblyElementsNumbers['head'])
        lc = g.calc_CoM_2D(d, elem=fmd.assemblyElementsNumbers['lateralcondyle'])
        mc = g.calc_CoM_2D(d, elem=fmd.assemblyElementsNumbers['medialcondyle'])
        alignedParams.append(
            alignment_analytic.alignAnatomic(g.get_field_parameters().squeeze().T, head, mc, lc).T[:, :, numpy.newaxis])

    return alignedParams


# =======================================================#
# pelvis alignment                                      #
# =======================================================#
def createPelvisACSISB(lasis, rasis, lpsis, rpsis):
    """Calculate the ISB pelvis anatomic coordinate system
    axes: x-anterior, y-superior, z-right
    """
    oa = (lasis + rasis) / 2.0
    op = (lpsis + lpsis) / 2.0
    # right
    z = normaliseVector(rasis - lasis)
    # anterior, in plane of op, rasis, lasis
    n1 = normaliseVector(numpy.cross(rasis - op, lasis - op))
    x = normaliseVector(numpy.cross(n1, z))
    # superior
    y = normaliseVector(numpy.cross(z, x))
    return oa, x, y, z


def createPelvisACSAPP(lasis, rasis, lpt, rpt):
    """Calculate the anterior pelvic plane anatomic
    coordinate system: x-right, y-anterior, z-superior
    """
    # lasis = numpy.array(lasis)
    # rasis = numpy.array(rasis)
    # lpt = numpy.array(lpt)
    # rpt = numpy.array(rpt)

    o = 0.5 * (lasis + rasis)
    pt = 0.5 * (lpt + rpt)
    x = normaliseVector(rasis - lasis)
    y = normaliseVector(numpy.cross(x, pt - o))
    # y = normaliseVector(numpy.cross(x, lpt-lasis))
    z = normaliseVector(numpy.cross(x, y))
    return o, x, y, z


def alignAnatomicPelvis(X, lasis, rasis, lpsis, rpsis, return_t=False):
    # oa = ( lasis + rasis )/2.0
    # op = ( lpsis + lpsis )/2.0
    # z = normaliseVector( rasis - lasis )
    # y = normaliseVector( numpy.cross( z, op - rasis ) )
    # x = normaliseVector( numpy.cross( y, z ) )

    o, x, y, z = createPelvisACSISB(lasis, rasis, lpsis, rpsis)

    u = numpy.array([o, o + x, o + y, o + z])
    ut = numpy.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    t = transform3D.directAffine(u, ut)
    if t.shape == (3, 4):
        t = numpy.vstack([t, [0, 0, 0, 1]])

    if return_t:
        return transform3D.transformAffine(X, t), t
    else:
        return transform3D.transformAffine(X, t)


def alignAnatomicPelvisAPP(X, lasis, rasis, lpt, rpt, return_t=False):
    """
    Align to the Anterior Pelvic Plane (APP) coordinate system commonly 
    used in hip surgery.

    The APP is defined by the LASIS, RPSIS, and the midpoint between left and
    right pubic tubercles. The x axis is parallel to LASIS-RASIS, the y axis is
    normal to the APP, and the z axis is normal to the x and y axes. The
    origin is the midpoint between LASIS and RASIS.
    """
    # lasis = numpy.array(lasis)
    # rasis = numpy.array(rasis)
    # lpt = numpy.array(lpt)
    # rpt = numpy.array(rpt)

    # o = 0.5*(lasis+rasis) 
    # pt = 0.5*(lpt + rpt)
    # x = normaliseVector(rasis-lasis)
    # y = normaliseVector(numpy.cross(x, pt-o))
    # z = normaliseVector(numpy.cross(x, y))

    o, x, y, z = createPelvisACSAPP(lasis, rasis, lpt, rpt)

    u = numpy.array([o, o + x, o + y, o + z])
    ut = numpy.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    t = transform3D.directAffine(u, ut)
    if t.shape == (3, 4):
        t = numpy.vstack([t, [0, 0, 0, 1]])

    if return_t:
        return transform3D.transformAffine(X, t), t
    else:
        return transform3D.transformAffine(X, t)


def alignAnatomicLH(X, LASIS, LPSIS, FHC):
    y = normaliseVector(LPSIS - FHC)
    x = normaliseVector(numpy.cross(y, LASIS - FHC))
    z = normaliseVector(numpy.cross(x, y))

    u = numpy.array([FHC, FHC + x, FHC + y, FHC + z])
    ut = numpy.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    t = transform3D.directAffine(u, ut)
    if t.shape == (3, 4):
        t = numpy.vstack([t, [0, 0, 0, 1]])
    return transform3D.transformAffine(X, t)


# pelvisLandmarkNodes = {'lasis': 1005,
#                     'rasis':  465,
#                     'lpsis':  924,
#                     'rpsis':  384,
#                     }

pelvisLandmarkNodes = {
    'lasis': fw_model_landmarks.PELVIS_LASIS_NODE,
    'rasis': fw_model_landmarks.PELVIS_RASIS_NODE,
    'lpsis': fw_model_landmarks.PELVIS_LPSIS_NODE,
    'rpsis': fw_model_landmarks.PELVIS_RPSIS_NODE,
    'lpt': fw_model_landmarks.PELVIS_LPT_NODE,
    'rpt': fw_model_landmarks.PELVIS_RPT_NODE,
}

# TODO: These values are NOT the left-hemi nodes.
#   Nor do they align with the left combined-pelvis nodes.
LHLandmarkNodes = {
    'lasis': 466,
    'lpsis': 384,
}

LHAcetabulumElements = [38, 39, 40, 41, 42]


def alignLHMeshParametersAnatomic(Gs):
    """
    three landmarks are the CoMs of the three pelvis bones
    """

    alignedParams = []
    d = (10, 10)
    for g in Gs:
        nodeCoords = g.get_all_point_positions()
        lasis = nodeCoords[LHLandmarkNodes['lasis']]
        lpsis = nodeCoords[LHLandmarkNodes['lpsis']]
        acetEP = g.evaluate_geometric_field_in_elements(d, LHAcetabulumElements).T
        FHC, FHRadius = alignment_fitting.fitSphere(acetEP)
        alignedParams.append(
            alignAnatomicLH(g.get_field_parameters().squeeze().T, lasis, lpsis, FHC).T[:, :, numpy.newaxis])

    return alignedParams


def alignWholePelvisMeshParametersAnatomicSingle(g):
    nodeCoords = g.get_all_point_positions()
    lasis = nodeCoords[pelvisLandmarkNodes['lasis']]
    rasis = nodeCoords[pelvisLandmarkNodes['rasis']]
    lpsis = nodeCoords[pelvisLandmarkNodes['lpsis']]
    rpsis = nodeCoords[pelvisLandmarkNodes['rpsis']]

    alignedParams, t = alignAnatomicPelvis(g.get_field_parameters().squeeze().T, lasis, rasis, lpsis, rpsis,
                                           return_t=True)
    alignedParams = alignedParams.T[:, :, numpy.newaxis]

    return alignedParams, t


def alignWholePelvisMeshParametersAnatomic(Gs):
    """
    three landmarks are the CoMs of the three pelvis bones
    """

    alignedParams = []
    for g in Gs:
        alignedParams.append(alignWholePelvisMeshParametersAnatomicSingle(g)[0])

    return alignedParams


def alignWholePelvisMeshParametersAnatomicAPPSingle(g):
    nodeCoords = g.get_all_point_positions()
    lasis = nodeCoords[pelvisLandmarkNodes['lasis']]
    rasis = nodeCoords[pelvisLandmarkNodes['rasis']]
    lpt = nodeCoords[pelvisLandmarkNodes['lpt']]
    rpt = nodeCoords[pelvisLandmarkNodes['rpt']]

    alignedParams, t = alignAnatomicPelvisAPP(g.get_field_parameters().squeeze().T,
                                              lasis, rasis, lpt, rpt,
                                              return_t=True
                                              )
    alignedParams = alignedParams.T[:, :, numpy.newaxis]

    return alignedParams, t


def alignWholePelvisMeshParametersAnatomicAPP(Gs):
    """
    three landmarks are the CoMs of the three pelvis bones
    """

    alignedParams = []
    for g in Gs:
        alignedParams.append(alignWholePelvisMeshParametersAnatomicAPPSingle(g)[0])

    return alignedParams


def alignPelvisLandmarksPC(gf, pc, landmarks, weights=1.0, gf_params_callback=None, mw0=1.0, mwn=1.0):
    """
    landmarks: a list of tuples [(landmark name, landmark coords),...]
    valid landmark names: LASIS, RASIS, LPSIS, RPSIS, Sacral, LHJC, RHJC
    """
    sourceGF = copy.deepcopy(gf)
    targetLandmarks = []
    ldObjs = []
    for ldName, ldTarg in landmarks:
        targetLandmarks.append(ldTarg)
        evaluator = fw_model_landmarks.make_landmark_evaluator('pelvis-' + ldName, sourceGF)
        ldObjs.append(_makeLandmarkObj(ldTarg, evaluator))

    def obj(P):
        P3 = P.reshape((3, -1))
        se = numpy.array([f(P3) for f in ldObjs])
        # print se
        sse = (se * weights).sum()
        return sse

    pcFitter = PCA_fitting.PCFit(pc=pc)
    pcFitter.useFMin = True
    pcFitter.ftol = 1e-6

    P0 = pc.getMean().reshape((3, -1))
    n0 = ldObjs[0](P0)
    x0 = numpy.hstack([targetLandmarks[0] - n0, 0, 0, 0])

    # targetCoM = (targetHC + ((targetMEC+targetLEC)/2.0))/2.0
    # x0 = numpy.hstack([targetCoM - sourceGF.calc_CoM(), 0, 0, 0])

    rigidT, rigidP = pcFitter.rigidFit(obj, x0=x0)
    sourceGF.set_field_parameters(rigidP.reshape((3, -1, 1)))
    rigidSSE = obj(rigidP)
    if gf_params_callback is not None:
        gf_params_callback(rigidP)

    rigidMode0T, rigidMode0P = pcFitter.rigidMode0Fit(obj, m_weight=mw0)
    sourceGF.set_field_parameters(rigidMode0P.reshape((3, -1, 1)))
    rigidMode0SSE = obj(rigidMode0P)
    if gf_params_callback is not None:
        gf_params_callback(rigidMode0P)

    rigidModeNT, rigidModeNP = pcFitter.rigidModeNFit(obj, modes=[1, 2], m_weight=mwn)
    sourceGF.set_field_parameters(rigidModeNP.reshape((3, -1, 1)))
    rigidModeNSSE = obj(rigidModeNP)
    if gf_params_callback is not None:
        gf_params_callback(rigidModeNP)

    return sourceGF, (rigidSSE, rigidMode0SSE, rigidModeNSSE), rigidModeNT


# ========================#
# Tibia fibula alignment #
# ========================#
def createTibiaFibulaACSGroodSuntay(MM, LM, MC, LC, side='left'):
    """Axes: medial, anterior, proximal
    """
    IC = (MC + LC) / 2.0
    IM = (MM + LM) / 2.0

    z = normaliseVector(IC - IM)
    if side == 'right':
        z *= -1.0
    y = normaliseVector(numpy.cross(z, MC - LC))
    x = normaliseVector(numpy.cross(y, z))

    return IC, x, y, z


def createTibiaFibulaACSISB(MM, LM, MC, LC, side='left'):
    """Axes: x-anterior, y-superior, z-right. Calcaneus CS
    """
    IC = (MC + LC) / 2.0
    IM = (MM + LM) / 2.0  # origin

    # superiorly, IM to IC
    y = normaliseVector(IC - IM)

    # anteriorly, normal to plane of IM, LC and MC
    x = normaliseVector(numpy.cross(LC - IM, MC - IM))

    # right
    z = normaliseVector(numpy.cross(x, y))
    if side == 'right':
        z *= -1.0
        x *= -1.0

    return IM, x, y, z


# TODO: Mostly same as above but in a different order.
#   Above implementation has issue with orthogonal vector.
#   ...
#   Might be best to just try get this into GIAS3 now.
#   Check if replacing the method above with this breaks anything (more than it is).
def createTibiaFibulaACSISB_2(MM, LM, MC, LC, side='left'):
    """Axes: x-anterior, y-superior, z-right. Calcaneus CS
    """

    IC = (MC + LC) / 2.0
    IM = (MM + LM) / 2.0  # origin

    # superiorly, IM to IC
    z = normaliseVector(MC - LC)
    n1 = normaliseVector(numpy.cross(normaliseVector(MC-IM), normaliseVector(LC-IM)))
    if side == 'right':
        z *= -1.0
        n1 *= -1.0

    y = normaliseVector(numpy.cross(n1, z))
    x = normaliseVector(numpy.cross(y, z))
    #print('tib:', z.dot(x), y.dot(z), x.dot(y))

    return IM, x, y, z


def createTibiaFibulaACSOpenSim(MM, LM, MC, LC, side='left'):
    """Axes: x-anterior, y-superior, z-right. Calcaneus CS
    """
    IC = (MC + LC) / 2.0  # origin
    IM = (MM + LM) / 2.0

    # superiorly, IM to IC
    y = normaliseVector(IC - IM)

    # anteriorly, normal to plane of IM, LC and MC
    x = normaliseVector(numpy.cross(LC - IM, MC - IM))

    # right
    z = normaliseVector(numpy.cross(x, y))
    if side == 'right':
        z *= -1.0
        x *= -1.0

    return IC, x, y, z


def alignAnatomicTibiaFibulaGroodSuntay(X, MM, LM, MC, LC, return_t=False):
    # IC = (MC + LC)/2.0
    # IM = (MM + LM)/2.0

    # z = normaliseVector(IC - IM)
    # y = normaliseVector(numpy.cross(z, MC-LC))
    # x = normaliseVector(numpy.cross(y, z))

    IC, x, y, z = createTibiaFibulaACSGroodSuntay(MM, LM, MC, LC)

    u = numpy.array([IC, IC + x, IC + y, IC + z])
    ut = numpy.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

    t = transform3D.directAffine(u, ut)
    if t.shape == (3, 4):
        t = numpy.vstack([t, [0, 0, 0, 1]])
    if return_t:
        return transform3D.transformAffine(X, t), t
    else:
        return transform3D.transformAffine(X, t)


def alignTibiaFibulaLandmarksPC(gf, pc, landmarks, weights=1.0, gf_params_callback=None, mw0=1.0, mwn=1.0):
    """
    landmarks: a list of tuples [(landmark name, landmark coords),...]
    valid landmark names: LM, MM, TT, kneecentre
    """
    sourceGF = copy.deepcopy(gf)
    targetLandmarks = []
    ldObjs = []
    for ldName, ldTarg in landmarks:
        targetLandmarks.append(ldTarg)
        evaluator = fw_model_landmarks.make_landmark_evaluator('tibiafibula-' + ldName, sourceGF)
        ldObjs.append(_makeLandmarkObj(ldTarg, evaluator))

    def obj(P):
        P3 = P.reshape((3, -1))
        se = numpy.array([f(P3) for f in ldObjs])
        # print se
        sse = (se * weights).sum()
        return sse

    pcFitter = PCA_fitting.PCFit(pc=pc)
    pcFitter.useFMin = True
    pcFitter.ftol = 1e-3

    P0 = pc.getMean().reshape((3, -1))
    n0 = ldObjs[0](P0)
    x0 = numpy.hstack([targetLandmarks[0] - n0, 0, 0, 0])

    # targetCoM = (targetHC + ((targetMEC+targetLEC)/2.0))/2.0
    # x0 = numpy.hstack([targetCoM - sourceGF.calc_CoM(), 0, 0, 0])

    rigidT, rigidP = pcFitter.rigidFit(obj, x0=x0)
    sourceGF.set_field_parameters(rigidP.reshape((3, -1, 1)))
    rigidSSE = obj(rigidP)
    if gf_params_callback is not None:
        gf_params_callback(rigidP)

    rigidMode0T, rigidMode0P = pcFitter.rigidMode0Fit(obj, m_weight=mw0)
    sourceGF.set_field_parameters(rigidMode0P.reshape((3, -1, 1)))
    rigidMode0SSE = obj(rigidMode0P)
    if gf_params_callback is not None:
        gf_params_callback(rigidMode0P)

    rigidModeNT, rigidModeNP = pcFitter.rigidModeNFit(obj, modes=[1, 2], m_weight=mwn)
    sourceGF.set_field_parameters(rigidModeNP.reshape((3, -1, 1)))
    rigidModeNSSE = obj(rigidModeNP)
    if gf_params_callback is not None:
        gf_params_callback(rigidModeNP)

    return sourceGF, (rigidSSE, rigidMode0SSE, rigidModeNSSE), rigidModeNT


# ===================#
# Patella alignment #
# ===================#
def createPatellaACSTest(sup, inf, lat, side='left'):
    """Axes: x-anterior, y-superior, z-right
    """
    o = (sup + inf) / 2.0
    y = normaliseVector(sup - inf)
    x = normaliseVector(numpy.cross(lat - inf, sup - inf))
    z = normaliseVector(numpy.cross(x, y))
    if side == 'right':
        z *= -1.0
    return o, x, y, z
