# RCS info
# $Author: garyg $
# $Locker:  $
# $Date: 2018/03/13 20:17:29 $
# $Id: cpc102_tsk060.make,v 1.8 2018/03/13 20:17:29 garyg Exp $
# $Revision: 1.8 $
# $State: Exp $


include $(MAKEINC)/make.common
include $(MAKEINC)/make.$(ARCH)

install:: 
	@if [ -d $(TOOLSCFGDIR) ]; then set +x; \
	else (set -x; $(MKDIR) $(TOOLSCFGDIR)); fi
	@if [ -d $(DATADIR) ]; then set +x; \
	else (set -x; $(MKDIR) $(DATADIR)); fi
	$(INSTALL) $(INSTDATFLAGS) bias_table.msg $(TOOLSCFGDIR)/bias_table.msg
	$(INSTALL) $(INSTDATFLAGS) one_time_req.msg $(TOOLSCFGDIR)/one_time_req.msg
	$(INSTALL) $(INSTDATFLAGS) awips_rps.msg $(TOOLSCFGDIR)/awips_rps.msg
	$(INSTALL) $(INSTDATFLAGS) rpccds_rps.msg $(TOOLSCFGDIR)/rpccds_rps.msg
	$(INSTALL) $(INSTDATFLAGS) model_data.msg $(TOOLSCFGDIR)/model_data.msg

BINMAKEFILES = nbtcp.mak awips2nbtcp.mak

include $(MAKEINC)/make.parent_bin

