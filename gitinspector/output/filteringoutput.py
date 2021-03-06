# coding: utf-8
#
# Copyright © 2012-2015 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from __future__ import unicode_literals
import textwrap

from ..filtering import __filters__, has_filtered
from ..localization import N_
from .. import terminal
from .outputable import Outputable


FILTERING_INFO_TEXT = N_("The following files were excluded from the statistics due to the specified exclusion patterns")
FILTERING_AUTHOR_INFO_TEXT = N_("The following authors were excluded from the statistics due to the specified exclusion patterns")
FILTERING_EMAIL_INFO_TEXT = N_("The authors with the following emails were excluded from the statistics due to the specified " \
                               "exclusion patterns")
FILTERING_COMMIT_INFO_TEXT = N_("The following commit revisions were excluded from the statistics due to the specified " \
                                "exclusion patterns")

class FilteringOutput(Outputable):
	@staticmethod
	def __output_html_section__(info_string, filtered):
		filtering_xml = ""

		if filtered:
			filtering_xml += "<p>" + info_string + "."+ "</p>"

			for i in filtered:
				filtering_xml += "<p>" + i + "</p>"

		return filtering_xml

	def output_html(self):
		if has_filtered():
			filtering_xml = "<div><div class=\"box\">"
			FilteringOutput.__output_html_section__(_(FILTERING_INFO_TEXT), __filters__["file"][1])
			FilteringOutput.__output_html_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__["author"][1])
			FilteringOutput.__output_html_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__["email"][1])
			FilteringOutput.__output_html_section__(_(FILTERING_COMMIT_INFO_TEXT), __filters__["revision"][1])
			filtering_xml += "</div></div>"

			print(filtering_xml)

	@staticmethod
	def __output_text_section__(info_string, filtered):
		if filtered:
			print("\n" + textwrap.fill(info_string + ":", width=terminal.get_size()[0]))

			for i in filtered:
				(width, _unused) = terminal.get_size()
				print("...%s" % i[-width+3:] if len(i) > width else i)

	def output_text(self):
		FilteringOutput.__output_text_section__(_(FILTERING_INFO_TEXT), __filters__["file"][1])
		FilteringOutput.__output_text_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__["author"][1])
		FilteringOutput.__output_text_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__["email"][1])
		FilteringOutput.__output_text_section__(_(FILTERING_COMMIT_INFO_TEXT), __filters__["revision"][1])

	@staticmethod
	def __output_xml_section__(info_string, filtered, container_tagname):
		if filtered:
			message_xml = "\t\t\t<message>" +info_string + "</message>\n"
			filtering_xml = ""

			for i in filtered:
				filtering_xml += "\t\t\t\t<entry>".format(container_tagname) + i + "</entry>\n".format(container_tagname)

			print("\t\t<{0}>".format(container_tagname))
			print(message_xml + "\t\t\t<entries>\n" + filtering_xml + "\t\t\t</entries>\n")
			print("\t\t</{0}>".format(container_tagname))

	def output_xml(self):
		if has_filtered():
			print("\t<filtering>")
			FilteringOutput.__output_xml_section__(_(FILTERING_INFO_TEXT), __filters__["file"][1], "files")
			FilteringOutput.__output_xml_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__["author"][1], "authors")
			FilteringOutput.__output_xml_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__["email"][1], "emails")
			FilteringOutput.__output_xml_section__(_(FILTERING_COMMIT_INFO_TEXT), __filters__["revision"][1], "revision")
			print("\t</filtering>")
