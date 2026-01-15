from frctools import Alliance
from frctools.frcmath import Vector2, Vector3, Quaternion
from .apriltags_nt import AprilTagsNetworkTable, AprilTagEntry

from typing import Any, List


class AprilTagDefinition:
	def __init__(self, id: int, size: float, position: Vector3, rotation: Quaternion):
		self.__id = id
		self.__size = size
		self.__position = position
		self.__rotation = rotation

	@property
	def id(self):
		return self.__id

	@property
	def size(self):
		return self.__size

	@property
	def position(self):
		return self.__position

	@property
	def rotation(self):
		return self.__rotation

	def __str__(self):
		return f'id:{self.id}, size:{self.size}, position:{self.position}, rotation:{self.rotation}'

	def __repr__(self):
		return f'AprilTagDefinition({str(self)})'


RAPIDREACT_2022_APRIL_TAGS = {
	0: AprilTagDefinition(0, 165.1, Vector3(-0.0035306, 7.578928199999999, 0.8858503999999999), Quaternion(0.0, 0.0, 0.0, 1.0)),
	1: AprilTagDefinition(1, 165.1, Vector3(3.2327088, 5.486654, 1.7254728), Quaternion(0.0, 0.0, 0.0, 1.0)),
	2: AprilTagDefinition(2, 165.1, Vector3(3.067812, 5.3305202, 1.3762228), Quaternion(0.0, 0.0, -0.7071067811865475, 0.7071067811865476)),
	3: AprilTagDefinition(3, 165.1, Vector3(0.0039878, 5.058536999999999, 0.80645), Quaternion(0.0, 0.0, 0.0, 1.0)),
	4: AprilTagDefinition(4, 165.1, Vector3(0.0039878, 3.5124898, 0.80645), Quaternion(0.0, 0.0, 0.0, 1.0)),
	5: AprilTagDefinition(5, 165.1, Vector3(0.12110719999999998, 1.7178274, 0.8906002000000001), Quaternion(0.0, 0.0, 0.39273842708457407, 0.9196502204050923)),
	6: AprilTagDefinition(6, 165.1, Vector3(0.8733027999999999, 0.9412985999999999, 0.8906002000000001), Quaternion(0.0, 0.0, 0.39273842708457407, 0.9196502204050923)),
	7: AprilTagDefinition(7, 165.1, Vector3(1.6150844, 0.15725139999999999, 0.8906002000000001), Quaternion(0.0, 0.0, 0.39273842708457407, 0.9196502204050923)),
	10: AprilTagDefinition(10, 165.1, Vector3(16.4627306, 0.6506718, 0.8858503999999999), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	11: AprilTagDefinition(11, 165.1, Vector3(13.2350002, 2.743454, 1.7254728), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	12: AprilTagDefinition(12, 165.1, Vector3(13.391388000000001, 2.8998418, 1.3762228), Quaternion(0.0, 0.0, 0.7071067811865475, 0.7071067811865476)),
	13: AprilTagDefinition(13, 165.1, Vector3(16.4552122, 3.1755079999999998, 0.80645), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	14: AprilTagDefinition(14, 165.1, Vector3(16.4552122, 4.7171356, 0.80645), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	15: AprilTagDefinition(15, 165.1, Vector3(16.3350194, 6.5149729999999995, 0.8937752), Quaternion(-0.0, 0.0, 0.9278362538989199, -0.37298778257580906)),
	16: AprilTagDefinition(16, 165.1, Vector3(15.5904946, 7.292695599999999, 0.8906002000000001), Quaternion(-0.0, 0.0, 0.9278362538989199, -0.37298778257580906)),
	17: AprilTagDefinition(17, 165.1, Vector3(14.847188999999998, 8.0691228, 0.8906002000000001), Quaternion(-0.0, 0.0, 0.9278362538989199, -0.37298778257580906)),
	40: AprilTagDefinition(40, 165.1, Vector3(7.874127, 4.9131728, 0.7032752), Quaternion(0.0, 0.0, 0.838670567945424, 0.5446390350150271)),
	41: AprilTagDefinition(41, 165.1, Vector3(7.4312271999999995, 3.759327, 0.7032752), Quaternion(-0.0, 0.0, 0.9781476007338057, -0.20791169081775934)),
	42: AprilTagDefinition(42, 165.1, Vector3(8.585073, 3.3164272, 0.7032752), Quaternion(0.0, 0.0, -0.5446390350150271, 0.838670567945424)),
	43: AprilTagDefinition(43, 165.1, Vector3(9.0279728, 4.470273, 0.7032752), Quaternion(0.0, 0.0, 0.20791169081775934, 0.9781476007338057)),
	50: AprilTagDefinition(50, 165.1, Vector3(7.6790296, 4.3261534, 2.4177244), Quaternion(-0.22744989571511945, 0.04215534644161733, 0.9565859910053995, 0.17729273396782605)),
	51: AprilTagDefinition(51, 165.1, Vector3(8.0182466, 3.5642296, 2.4177244), Quaternion(-0.19063969497246985, -0.13102303230819815, 0.8017733354717242, -0.5510435465842192)),
	52: AprilTagDefinition(52, 165.1, Vector3(8.7801704, 3.9034466, 2.4177244), Quaternion(-0.04215534644161739, -0.22744989571511942, 0.17729273396782633, -0.9565859910053994)),
	53: AprilTagDefinition(53, 165.1, Vector3(8.4409534, 4.6653704, 2.4177244), Quaternion(-0.1310230323081982, 0.19063969497246983, 0.5510435465842194, 0.8017733354717241)),
}

CHARGEDUP_2023_APRIL_TAGS = {
	1: AprilTagDefinition(1, 165.1, Vector3(15.513558, 1.071626, 0.462788), Quaternion(0.0, 0.0, 1.0, 0.0)),
	2: AprilTagDefinition(2, 165.1, Vector3(15.513558, 2.748026, 0.462788), Quaternion(0.0, 0.0, 1.0, 0.0)),
	3: AprilTagDefinition(3, 165.1, Vector3(15.513558, 4.424426, 0.462788), Quaternion(0.0, 0.0, 1.0, 0.0)),
	4: AprilTagDefinition(4, 165.1, Vector3(16.178784, 6.749796, 0.695452), Quaternion(0.0, 0.0, 1.0, 0.0)),
	5: AprilTagDefinition(5, 165.1, Vector3(0.36195, 6.749796, 0.695452), Quaternion(0.0, 0.0, 0.0, 1.0)),
	6: AprilTagDefinition(6, 165.1, Vector3(1.02743, 4.424426, 0.462788), Quaternion(0.0, 0.0, 0.0, 1.0)),
	7: AprilTagDefinition(7, 165.1, Vector3(1.02743, 2.748026, 0.462788), Quaternion(0.0, 0.0, 0.0, 1.0)),
	8: AprilTagDefinition(8, 165.1, Vector3(1.02743, 1.071626, 0.462788), Quaternion(0.0, 0.0, 0.0, 1.0)),
}

CRESCENDO_2024_APRIL_TAGS = {
	1: AprilTagDefinition(1, 165.1, Vector3(15.079472, 0.245872, 1.355852), Quaternion(0., 0., 0.8660254037844386, 0.5)),
	2: AprilTagDefinition(2, 165.1, Vector3(16.185134, 0.883666, 1.355852), Quaternion(0., 0., 0.8660254037844386, 0.5)),
	3: AprilTagDefinition(3, 165.1, Vector3(16.579342, 4.982718, 1.451102), Quaternion(0., 0., 1., 0.)),
	4: AprilTagDefinition(4, 165.1, Vector3(16.579342, 5.547868, 1.451102), Quaternion(0., 0., 1., 0.)),
	5: AprilTagDefinition(5, 165.1, Vector3(14.700758, 8.2042, 1.355852), Quaternion(0., 0., 0.7071067811865476, -0.7071067811865475)),
	6: AprilTagDefinition(6, 165.1, Vector3(1.8415, 8.2042, 1.355852), Quaternion(0., 0., 0.7071067811865476, -0.7071067811865475)),
	7: AprilTagDefinition(7, 165.1, Vector3(-0.0381, 5.547868, 1.451102), Quaternion(0., 0., 0., 1.)),
	8: AprilTagDefinition(8, 165.1, Vector3(-0.0381, 4.982718, 1.451102), Quaternion(0., 0., 0., 1.)),
	9: AprilTagDefinition(9, 165.1, Vector3(0.356108, 0.883666, 1.355852), Quaternion(0., 0., 0.5, 0.8660254037844387)),
	10: AprilTagDefinition(10, 165.1, Vector3(1.461516, 0.245872, 1.355852), Quaternion(0., 0., 0.5, 0.8660254037844387)),
	11: AprilTagDefinition(11, 165.1, Vector3(11.904726, 3.713226, 1.3208), Quaternion(0., 0., 0.5, -0.8660254037844387)),
	12: AprilTagDefinition(12, 165.1, Vector3(11.904726, 4.49834, 1.3208), Quaternion(0., 0., 0.5, 0.8660254037844387)),
	13: AprilTagDefinition(13, 165.1, Vector3(11.220196, 4.105148, 1.3208), Quaternion(0., 0., 1., 0.)),
	14: AprilTagDefinition(14, 165.1, Vector3(5.320792, 4.105148, 1.3208), Quaternion(0., 0., 0., 1.)),
	15: AprilTagDefinition(15, 165.1, Vector3(4.641342, 4.49834, 1.3208), Quaternion(0., 0., 0.8660254037844386, 0.5)),
	16: AprilTagDefinition(16, 165.1, Vector3(4.641342, 3.713226, 1.3208), Quaternion(0., 0., 0.8660254037844386, -0.5)),
}

REEFSCAPE_2025_APRIL_TAGS = {
	1: AprilTagDefinition(1, 165.1, Vector3(16.697198, 0.65532, 1.4859), Quaternion(0.0, 0.0, 0.8910065241883678, 0.4539904997395468)),
	2: AprilTagDefinition(2, 165.1, Vector3(16.697198, 7.3964799999999995, 1.4859), Quaternion(-0.0, 0.0, 0.8910065241883679, -0.45399049973954675)),
	3: AprilTagDefinition(3, 165.1, Vector3(11.560809999999998, 8.05561, 1.30175), Quaternion(-0.0, 0.0, 0.7071067811865476, -0.7071067811865475)),
	4: AprilTagDefinition(4, 165.1, Vector3(9.276079999999999, 6.137656, 1.8679160000000001), Quaternion(0.0, 0.25881904510252074, 0.0, 0.9659258262890683)),
	5: AprilTagDefinition(5, 165.1, Vector3(9.276079999999999, 1.914906, 1.8679160000000001), Quaternion(0.0, 0.25881904510252074, 0.0, 0.9659258262890683)),
	6: AprilTagDefinition(6, 165.1, Vector3(13.474446, 3.3063179999999996, 0.308102), Quaternion(-0.0, 0.0, 0.49999999999999994, -0.8660254037844387)),
	7: AprilTagDefinition(7, 165.1, Vector3(13.890498, 4.0259, 0.308102), Quaternion(0.0, 0.0, 0.0, 1.0)),
	8: AprilTagDefinition(8, 165.1, Vector3(13.474446, 4.745482, 0.308102), Quaternion(0.0, 0.0, 0.49999999999999994, 0.8660254037844387)),
	9: AprilTagDefinition(9, 165.1, Vector3(12.643358, 4.745482, 0.308102), Quaternion(0.0, 0.0, 0.8660254037844386, 0.5000000000000001)),
	10: AprilTagDefinition(10, 165.1, Vector3(12.227305999999999, 4.0259, 0.308102), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	11: AprilTagDefinition(11, 165.1, Vector3(12.643358, 3.3063179999999996, 0.308102), Quaternion(-0.0, 0.0, 0.8660254037844387, -0.4999999999999998)),
	12: AprilTagDefinition(12, 165.1, Vector3(0.851154, 0.65532, 1.4859), Quaternion(0.0, 0.0, 0.45399049973954675, 0.8910065241883679)),
	13: AprilTagDefinition(13, 165.1, Vector3(0.851154, 7.3964799999999995, 1.4859), Quaternion(-0.0, 0.0, 0.45399049973954686, -0.8910065241883678)),
	14: AprilTagDefinition(14, 165.1, Vector3(8.272272, 6.137656, 1.8679160000000001), Quaternion(-0.25881904510252074, 1.5848095757158825e-17, 0.9659258262890683, 5.914589856893349e-17)),
	15: AprilTagDefinition(15, 165.1, Vector3(8.272272, 1.914906, 1.8679160000000001), Quaternion(-0.25881904510252074, 1.5848095757158825e-17, 0.9659258262890683, 5.914589856893349e-17)),
	16: AprilTagDefinition(16, 165.1, Vector3(5.9875419999999995, -0.0038099999999999996, 1.30175), Quaternion(0.0, 0.0, 0.7071067811865476, 0.7071067811865476)),
	17: AprilTagDefinition(17, 165.1, Vector3(4.073905999999999, 3.3063179999999996, 0.308102), Quaternion(-0.0, 0.0, 0.8660254037844387, -0.4999999999999998)),
	18: AprilTagDefinition(18, 165.1, Vector3(3.6576, 4.0259, 0.308102), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	19: AprilTagDefinition(19, 165.1, Vector3(4.073905999999999, 4.745482, 0.308102), Quaternion(0.0, 0.0, 0.8660254037844386, 0.5000000000000001)),
	20: AprilTagDefinition(20, 165.1, Vector3(4.904739999999999, 4.745482, 0.308102), Quaternion(0.0, 0.0, 0.49999999999999994, 0.8660254037844387)),
	21: AprilTagDefinition(21, 165.1, Vector3(5.321046, 4.0259, 0.308102), Quaternion(0.0, 0.0, 0.0, 1.0)),
	22: AprilTagDefinition(22, 165.1, Vector3(4.904739999999999, 3.3063179999999996, 0.308102), Quaternion(-0.0, 0.0, 0.49999999999999994, -0.8660254037844387)),
}

REBUILT_2026_APRIL__TAGS = {
	1: AprilTagDefinition(1, 165.1, Vector3(11.8779798, 7.4247756, 0.889), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	2: AprilTagDefinition(2, 165.1, Vector3(11.9154194, 4.638039999999999, 1.12395), Quaternion(0.0, 0.0, 0.7071067811865476, 0.7071067811865476)),
	3: AprilTagDefinition(3, 165.1, Vector3(11.3118646, 4.3902376, 1.12395), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	4: AprilTagDefinition(4, 165.1, Vector3(11.3118646, 4.0346376, 1.12395), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	5: AprilTagDefinition(5, 165.1, Vector3(11.9154194, 3.4312351999999997, 1.12395), Quaternion(-0.0, 0.0, 0.7071067811865476, -0.7071067811865475)),
	6: AprilTagDefinition(6, 165.1, Vector3(11.8779798, 0.6444996, 0.889), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	7: AprilTagDefinition(7, 165.1, Vector3(11.9528844, 0.6444996, 0.889), Quaternion(0.0, 0.0, 0.0, 1.0)),
	8: AprilTagDefinition(8, 165.1, Vector3(12.2710194, 3.4312351999999997, 1.12395), Quaternion(-0.0, 0.0, 0.7071067811865476, -0.7071067811865475)),
	9: AprilTagDefinition(9, 165.1, Vector3(12.519177399999998, 3.6790375999999996, 1.12395), Quaternion(0.0, 0.0, 0.0, 1.0)),
	10: AprilTagDefinition(10, 165.1, Vector3(12.519177399999998, 4.0346376, 1.12395), Quaternion(0.0, 0.0, 0.0, 1.0)),
	11: AprilTagDefinition(11, 165.1, Vector3(12.2710194, 4.638039999999999, 1.12395), Quaternion(0.0, 0.0, 0.7071067811865476, 0.7071067811865476)),
	12: AprilTagDefinition(12, 165.1, Vector3(11.9528844, 7.4247756, 0.889), Quaternion(0.0, 0.0, 0.0, 1.0)),
	13: AprilTagDefinition(13, 165.1, Vector3(16.5333172, 7.4033126, 0.55245), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	14: AprilTagDefinition(14, 165.1, Vector3(16.5333172, 6.9715126, 0.55245), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	15: AprilTagDefinition(15, 165.1, Vector3(16.5329616, 4.3235626, 0.55245), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	16: AprilTagDefinition(16, 165.1, Vector3(16.5329616, 3.8917626, 0.55245), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	17: AprilTagDefinition(17, 165.1, Vector3(4.6630844, 0.6444996, 0.889), Quaternion(0.0, 0.0, 0.0, 1.0)),
	18: AprilTagDefinition(18, 165.1, Vector3(4.6256194, 3.4312351999999997, 1.12395), Quaternion(-0.0, 0.0, 0.7071067811865476, -0.7071067811865475)),
	19: AprilTagDefinition(19, 165.1, Vector3(5.229174199999999, 3.6790375999999996, 1.12395), Quaternion(0.0, 0.0, 0.0, 1.0)),
	20: AprilTagDefinition(20, 165.1, Vector3(5.229174199999999, 4.0346376, 1.12395), Quaternion(0.0, 0.0, 0.0, 1.0)),
	21: AprilTagDefinition(21, 165.1, Vector3(4.6256194, 4.638039999999999, 1.12395), Quaternion(0.0, 0.0, 0.7071067811865476, 0.7071067811865476)),
	22: AprilTagDefinition(22, 165.1, Vector3(4.6630844, 7.4247756, 0.889), Quaternion(0.0, 0.0, 0.0, 1.0)),
	23: AprilTagDefinition(23, 165.1, Vector3(4.5881798, 7.4247756, 0.889), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	24: AprilTagDefinition(24, 165.1, Vector3(4.2700194, 4.638039999999999, 1.12395), Quaternion(0.0, 0.0, 0.7071067811865476, 0.7071067811865476)),
	25: AprilTagDefinition(25, 165.1, Vector3(4.0218614, 4.3902376, 1.12395), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	26: AprilTagDefinition(26, 165.1, Vector3(4.0218614, 4.0346376, 1.12395), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	27: AprilTagDefinition(27, 165.1, Vector3(4.2700194, 3.4312351999999997, 1.12395), Quaternion(-0.0, 0.0, 0.7071067811865476, -0.7071067811865475)),
	28: AprilTagDefinition(28, 165.1, Vector3(4.5881798, 0.6444996, 0.889), Quaternion(0.0, 0.0, 1.0, 6.123233995736766e-17)),
	29: AprilTagDefinition(29, 165.1, Vector3(0.0077469999999999995, 0.6659626, 0.55245), Quaternion(0.0, 0.0, 0.0, 1.0)),
	30: AprilTagDefinition(30, 165.1, Vector3(0.0077469999999999995, 1.0977626, 0.55245), Quaternion(0.0, 0.0, 0.0, 1.0)),
	31: AprilTagDefinition(31, 165.1, Vector3(0.0080772, 3.7457125999999996, 0.55245), Quaternion(0.0, 0.0, 0.0, 1.0)),
	32: AprilTagDefinition(32, 165.1, Vector3(0.0080772, 4.1775126, 0.55245), Quaternion(0.0, 0.0, 0.0, 1.0))
}


class AprilTagsFieldPose:
	def __init__(self, red_id: int, blue_id: int, tags_definition):
		self.__red_tag_nt = AprilTagsNetworkTable.get_tag(red_id)
		self.__red_tag_def = tags_definition[red_id]

		self.__blue_tag_nt = AprilTagsNetworkTable.get_tag(blue_id)
		self.__blue_tag_def = tags_definition[blue_id]

		self.__current_nt = None
		self.__current_def = None

	@property
	def nt(self) -> AprilTagEntry:
		return self.__current_nt

	@property
	def definition(self) -> AprilTagDefinition:
		return self.__current_def

	@property
	def id(self) -> int:
		return self.definition.id

	@property
	def is_detected(self) -> bool:
		return self.nt.is_detected()

	@property
	def center(self) -> Vector2:
		return self.nt.get_center()

	@property
	def relative_position(self) -> Vector3:
		return self.nt.get_position()

	@property
	def absolute_position(self) -> Vector3:
		raise NotImplementedError()

	@property
	def relative_rotation(self) -> Quaternion:
		return self.nt.get_rotation()

	@property
	def absolute_rotation(self) -> Quaternion:
		raise NotImplementedError()

	def refresh_alliance(self):
		ally = Alliance.get_alliance()

		if ally == Alliance.UNDEFINED:
			self.__current_nt = None
			self.__current_def = None
		elif ally == Alliance.RED:
			self.__current_nt = self.__red_tag_nt
			self.__current_def = self.__red_tag_def
		elif ally == Alliance.BLUE:
			self.__current_nt = self.__blue_tag_nt
			self.__current_def = self.__blue_tag_def

	def __str__(self):
		return f'red:{self.__red_tag_def.id} blue:{self.__blue_tag_def.id}'

	def __repr__(self):
		return f'AprilTagsFieldPose({str(self)})'


class AprilTagsBaseField:
	__INSTANCE__: 'AprilTagsBaseField' = None

	@classmethod
	def instance(cls) -> Any:
		if cls.__INSTANCE__ is None:
			cls.__INSTANCE__ = cls()

		return cls.__INSTANCE__


class AprilTagsBaseFieldModule:
	def __init__(self, tags: List[AprilTagsFieldPose]):
		self.__tags = tags

	@property
	def all(self):
		return self.__tags

	@property
	def detected(self):
		return [x for x in self.__tags if x.is_detected]

	def __getitem__(self, item):
		return self.__tags[item]

	def __iter__(self):
		for tag in self.__tags:
			yield tag


class AprilTagsReefscapeField(AprilTagsBaseField):
	class Reef(AprilTagsBaseFieldModule):
		def __init__(self):
			super().__init__([
				AprilTagsFieldPose(10, 21, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(9, 22, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(8, 17, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(7, 18, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(6, 19, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(11, 20, REEFSCAPE_2025_APRIL_TAGS)
			])

		@property
		def a(self):
			return self[0]

		@property
		def b(self):
			return self[1]

		@property
		def c(self):
			return self[2]

		@property
		def d(self):
			return self[3]

		@property
		def e(self):
			return self[4]

		@property
		def f(self):
			return self[5]

	class CoralStation(AprilTagsBaseFieldModule):
		def __init__(self):
			super().__init__([
				AprilTagsFieldPose(1, 13, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(2, 12, REEFSCAPE_2025_APRIL_TAGS)
			])

		@property
		def left(self):
			return self[0]

		@property
		def right(self):
			return self[1]

	class Cage(AprilTagsBaseFieldModule):
		def __init__(self):
			super().__init__([
				AprilTagsFieldPose(5, 14, REEFSCAPE_2025_APRIL_TAGS),
				AprilTagsFieldPose(4, 15, REEFSCAPE_2025_APRIL_TAGS)
			])

		@property
		def left(self):
			return self[0]

		@property
		def right(self):
			return self[1]

	def __init__(self):
		self.__reef = AprilTagsReefscapeField.Reef()
		self.__coral_station = AprilTagsReefscapeField.CoralStation()
		self.__cage = AprilTagsReefscapeField.Cage()
		self.__processor_tags = AprilTagsFieldPose(3, 16, REEFSCAPE_2025_APRIL_TAGS)

	def __get_reef__(self):
		return self.__reef
	@staticmethod
	def get_reef():
		return AprilTagsReefscapeField.instance().__get_reef__()

	def __get_coral_station__(self):
		return self.__coral_station
	@staticmethod
	def get_coral_station():
		return AprilTagsReefscapeField.instance().__get_coral_station__()

	def __get_cage__(self):
		return self.__cage
	@staticmethod
	def get_cage():
		return AprilTagsReefscapeField.instance().__get_cage__()

	def __get_processor_tags__(self):
		return self.__processor_tags
	@staticmethod
	def get_processor_tags():
		return AprilTagsReefscapeField.instance().__get_processor_tags__()

	def __refresh_alliance__(self):
		for t in self.__reef:
			t.refresh_alliance()

		for t in self.__coral_station:
			t.refresh_alliance()

		for t in self.__cage:
			t.refresh_alliance()

		self.__processor_tags.refresh_alliance()
	@staticmethod
	def refresh_alliance():
		AprilTagsReefscapeField.instance().__refresh_alliance__()

	@classmethod
	def instance(cls) -> 'AprilTagsReefscapeField':
		if AprilTagsNetworkTable.instance() is None:
			AprilTagsNetworkTable(22)

		return super(cls, cls).instance()
