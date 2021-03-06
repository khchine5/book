.. doctest docs/specs/noi/tickets.rst
.. _noi.specs.tickets:

=============================
Ticket management in Lino Noi
=============================

.. doctest init:
    >>> import lino
    >>> lino.startup('lino_book.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions implemented in
:mod:`lino_xl.lib.tickets` (as used by Lino Noi).



.. contents::
  :local:

.. currentmodule:: lino_xl.lib.tickets


Tickets
=======

A **Ticket** is a concrete question or problem formulated by a
user.  It is the smallest unit of work.  The user may be a system
user or an end user represented by a system user.

There are many tables used to show lists of tickets.        


.. class:: Ticket

    .. attribute:: user

        The author. The user who reported this ticket to the database
        and is responsible for managing it.

    .. attribute:: end_user

        The end user who is asking for help.

    .. attribute:: assigned_to

        The user who is working on this ticket.

    .. attribute:: state

        The state of this ticket. See :class:`TicketStates
        <lino_xl.lib.tickets.choicelists.TicketStates>`

    .. attribute:: waiting_for

        What to do next. An unformatted one-line text which describes
        what this ticket is waiting for.

    .. attribute:: upgrade_notes

        A formatted text field meant for writing instructions for the
        hoster's site administrator when doing an upgrade where this
        ticket is being deployed.

    .. attribute:: description

        A complete and concise description of the ticket. This should
        describe in more detail what this ticket is about. If the
        ticket has evolved during time, it should reflect the latest
        version.

        The description can contain *memo commands* defined by the
        application.

    .. attribute:: duplicate_of

        A pointer to the ticket which is the cause of this ticket.

        A ticket with a non-empty :attr:`duplicate_of` field can be
        called a "duplicate".  The number of a duplicate is
        theoretically higher than the number of the ticket it
        duplicates.

        The :attr:`state` of a duplicate does not automatically become
        that of the duplicated ticket.  Each ticket continues to have
        its own state. Example: Some long time ago, with Mathieu, we
        agreed that ticket #100 can go to *Sleeping*. Now Aurélie
        reported the same problem again as #904. This means that we
        should talk about it. And even before talking with her, I'd
        like to have a look at the code in order to estimate whether
        it is difficult or not, so I set the state of #904 to ToDo.

        Wouldn't it be preferrable to replace the :attr:`duplicate_of
        field by a :class:`LinkType
        <lino_xl.lib.tickets.choicelists.LinkTypes>` called
        "Duplicated/Duplicated by"?  No. We had this before and
        preferred the field, because a field is at least one click
        less, and because we *want* users to define a clear hiearchy
        with a clear root ticket. You can have a group of tickets
        which are all direct or indirect duplicates of this "root of
        all other problems".

    .. attribute:: deadline

        Specify that the ticket must be done for a given date.

        TODO: Triagers should have a table of tickets having this
        field non-empty and are still in an active state.

    .. attribute:: priority

        How urgent this ticket is. This should be a value between 0
        and 100.

    .. attribute:: rating

        How the author rates this ticket.

    .. attribute:: reporting_type

        An indication about who is going to pay for work on this
        site.  See :class:`ReportingTypes`.
        



.. class:: Tickets

    Base class for all tables of all tickets.

    .. attribute:: site

        Select a site if you want to see only tickets for this site.

    .. attribute:: show_private

        Show only (or hide) tickets that are marked private.

    .. attribute:: show_todo

        Show only (or hide) tickets which are todo (i.e. state is New
        or ToDo).

    .. attribute:: show_active

        Show only (or hide) tickets which are active (i.e. state is Talk
        or ToDo).

    .. attribute:: show_assigned

        Show only (or hide) tickets that are assigned to somebody.

    .. attribute:: has_site

        Show only (or hide) tickets which have a site assigned.

    .. attribute:: feasable_by

        Show only tickets for which the given supplier is competent.

           
.. class:: AllTickets

    Shows all tickets.
    
.. class:: RefTickets
           
    Shows all tickets that have a reference.

.. class:: PublicTickets
           
    Shows all public tickets.

.. class:: TicketsToTriage

    Shows tickets that need to be triaged.  Currently this is
    equivalent to those having their state set to :attr:`new
    <TicketStates.new>`.

.. class:: TicketsToTalk

.. class:: UnassignedTickets
.. class:: ActiveTickets

    Show all tickets that are in an active state.

.. class:: MyTickets
           
    Show all active tickets reported by me.

    >>> rt.login('jean').show(tickets.MyTickets)
    ... #doctest: -REPORT_UDIFF
    ========== ========================================================================================================= ============================================
     Priority   Description                                                                                               Workflow
    ---------- --------------------------------------------------------------------------------------------------------- --------------------------------------------
     Normal     `#115 (☉     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Luc <Detail>`__      [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
     Normal     `#106 (☎     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Jean <Detail>`__     [▶] **Talk** → [☾] [☉] [☐] [☒]
     Normal     `#100 (⚒     Cannot delete foo) <Detail>`__, assigned to `Mathieu <Detail>`__                             [✋] [▶] **Started** → [☾] [☐] [☒]
     Normal     `#97 (⛶     'NoneType' object has no attribute 'isocode') <Detail>`__                                     [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
     Normal     `#94 (☐     How can I see where bar?) <Detail>`__, assigned to `Jean <Detail>`__                          [▶] **Ready** → [☒]
     Normal     `#91 (☉     Cannot delete foo) <Detail>`__, assigned to `Luc <Detail>`__                                  [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
     Normal     `#82 (☎     Cannot delete foo) <Detail>`__, assigned to `Jean <Detail>`__                                 [▶] **Talk** → [☾] [☉] [☐] [☒]
     Normal     `#76 (⚒     How can I see where bar?) <Detail>`__, assigned to `Mathieu <Detail>`__                       [✋] [▶] **Started** → [☾] [☐] [☒]
     Normal     `#73 (⛶     Cannot delete foo) <Detail>`__                                                                [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
     Normal     `#70 (☐     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Jean <Detail>`__      [▶] **Ready** → [☒]
     Normal     `#67 (☉     How can I see where bar?) <Detail>`__, assigned to `Luc <Detail>`__                           [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
     Normal     `#58 (☎     How can I see where bar?) <Detail>`__, assigned to `Jean <Detail>`__                          [▶] **Talk** → [☾] [☉] [☐] [☒]
     Normal     `#52 (⚒     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Mathieu <Detail>`__   [✋] [▶] **Started** → [☾] [☐] [☒]
     Normal     `#49 (⛶     How can I see where bar?) <Detail>`__                                                         [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
     Normal     `#46 (☐     Cannot delete foo) <Detail>`__, assigned to `Jean <Detail>`__                                 [▶] **Ready** → [☒]
     Normal     `#43 (☉     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Luc <Detail>`__       [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
     Normal     `#34 (☎     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Jean <Detail>`__      [▶] **Talk** → [☾] [☉] [☐] [☒]
     Normal     `#28 (⚒     Cannot delete foo) <Detail>`__, assigned to `Mathieu <Detail>`__                              [✋] [▶] **Started** → [☾] [☐] [☒]
     Normal     `#25 (⛶     'NoneType' object has no attribute 'isocode') <Detail>`__                                     [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
     Normal     `#22 (☐     How can I see where bar?) <Detail>`__, assigned to `Jean <Detail>`__                          [▶] **Ready** → [☒]
     Normal     `#19 (☉     Cannot delete foo) <Detail>`__, assigned to `Luc <Detail>`__                                  [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
     Normal     `#10 (☎ Where can I find a Foo when bazing Bazes?) <Detail>`__, assigned to `Jean <Detail>`__             [▶] **Talk** → [☾] [☉] [☐] [☒]
     Normal     `#4 (⚒ Foo and bar don't baz) <Detail>`__, assigned to `Mathieu <Detail>`__                               [✋] [▶] **Started** → [☾] [☐] [☒]
     Normal     `#1 (⛶ Föö fails to bar when baz) <Detail>`__                                                             [✋] [■] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
    ========== ========================================================================================================= ============================================
    <BLANKLINE>


    

.. class:: TicketsByEndUser           
.. class:: TicketsByType
           
.. class:: DuplicatesByTicket

    Shows the tickets which are marked as duplicates of this
    (i.e. whose `duplicate_of` field points to this ticket.


.. class:: TicketsSummary

    Abstract base class for ticket tables with a summary.
    
.. class:: MyTicketsToWork
           
    Show all active tickets assigned to me.


.. class:: TicketsBySite    

           

Ticket types
============


.. class:: TicketType
.. class:: TicketTypes
           

Ticket states
=============


.. class:: TicketStates

    The choicelist of possible values for the :attr:`state
    <Ticket.state>` of a ticket.

    Default choices are:

    .. attribute:: new

        Somebody reported this ticket, but there was no response so
        far.
        The ticket needs to be triaged.

    .. attribute:: talk

        Some worker needs discussion with the author.  We don't yet
        know exactly what to do with it.

    .. attribute:: todo

        The ticket is confirmed and we are working on it.
        It appears in the todo list of somebody (either the assigned
        worker, or our general todo list)

    .. attribute:: testing

        The ticket is theoretically done, but we want to confirm this
        somehow, and it is not clear who should do the next step. If
        it is clear that the author should do the testing, then you
        should rather set the ticket to :attr:`talk`. If it is clear
        that you (the assignee) must test it, then leave the ticket at
        :attr:`todo`.

    .. attribute:: sleeping

        Waiting for some external event. We didn't decide what to do
        with it.

    .. attribute:: ready

        The ticket is basically :attr:`done`, but some detail still
        needs to be done by the :attr:`user` (e.g. testing,
        confirmation, documentation,..)

    .. attribute:: done

        The ticket has been done.

    .. attribute:: cancelled

        It has been decided that we won't fix this ticket.

You can see this table in your web interface using
:menuselection:`Explorer --> Tickets --> States`.

.. >>> show_menu_path(tickets.TicketStates)
   Explorer --> Tickets --> States

In a default configuration it defines the following choices:

>>> rt.show(tickets.TicketStates)
======= =========== ========== ======== ========
 value   name        text       Symbol   Active
------- ----------- ---------- -------- --------
 10      new         New        ⛶        Yes
 15      talk        Talk       ☎        Yes
 20      opened      Open       ☉        Yes
 22      started     Started    ⚒        Yes
 30      sleeping    Sleeping   ☾        No
 40      ready       Ready      ☐        Yes
 50      closed      Closed     ☑        No
 60      cancelled   Refused    ☒        No
======= =========== ========== ======== ========
<BLANKLINE>

Above table in German:

>>> rt.show(tickets.TicketStates, language="de")
====== =========== =============== ======== =======
 Wert   name        Text            Symbol   Aktiv
------ ----------- --------------- -------- -------
 10     new         Neu             ⛶        Ja
 15     talk        Besprechen      ☎        Ja
 20     opened      Offen           ☉        Ja
 22     started     Gestartet       ⚒        Ja
 30     sleeping    Schläft         ☾        Nein
 40     ready       Bereit          ☐        Ja
 50     closed      Abgeschlossen   ☑        Nein
 60     cancelled   Abgelehnt       ☒        Nein
====== =========== =============== ======== =======
<BLANKLINE>

There is also a "modern" series of symbols, which can be enabled
site-wide in :attr:`lino.core.site.Site.use_new_unicode_symbols`.
   


- :attr:`standby <lino_xl.lib.tickets.models.Ticket.standby>`




Sites
=====

Lino Noi has a list of "sites".  A site is a place where work is being
done.  This can be a concrete website on a server with a domain name,
but actually it can be anything your team uses for grouping their
tickets into more long-term "tasks" or "projects".

The site of a ticket also indicates "who is going to pay" for it.
Lino Noi does not issue invoices, so it uses this information only for
reporting about it and helping with the decision about whether and how
worktime is being invoiced to the customer.


.. class:: Site
           
.. class:: Subscription

    .. attribute:: site

        The site.
                   
    .. attribute:: user

        The user.
                   
    .. attribute:: primary

        Whether this is the primary subscription of this user.

        Checking this field will automatically uncheck any 
        previous primary subscriptions.
           


Here is a list of the sites in our demo database:

>>> rt.show(tickets.Sites)
============= ======== ================ ======== ========== ====
 Designation   Client   Contact person   Remark   Workflow   ID
------------- -------- ---------------- -------- ---------- ----
 pypi          pypi                                          3
 welket        welket                                        1
 welsch        welsch                                        2
============= ======== ================ ======== ========== ====
<BLANKLINE>

Developers can start working on tickets without specifying a site.
But after some time every ticket should get assigned to some site. You
can see a list of tickets which have not yet been assigned to a site:

>>> pv = dict(has_site=dd.YesNo.no)
>>> rt.show(tickets.AllTickets, param_values=pv)
... #doctest: +REPORT_UDIFF +ELLIPSIS
===== ============================================== ========== ============= ======
 ID    Summary                                        Priority   Workflow      Site
----- ---------------------------------------------- ---------- ------------- ------
 116   Foo never bars                                 Normal     **Started**
 114   Default account in invoices per partner        Normal     **Talk**
 112   How can I see where bar?                       Normal     **Refused**
 110   Why is foo so bar                              Normal     **Ready**
 108   No more foo when bar is gone                   Normal     **Started**
 106   'NoneType' object has no attribute 'isocode'   Normal     **Talk**
 104   Misc optimizations in Baz                      Normal     **Refused**
 102   Irritating message when bar                    Normal     **Ready**
 100   Cannot delete foo                              Normal     **Started**
 98    Foo never bars                                 Normal     **Talk**
 96    Default account in invoices per partner        Normal     **Refused**
 ...
 28    Cannot delete foo                              Normal     **Started**
 26    Foo never bars                                 Normal     **Talk**
 24    Default account in invoices per partner        Normal     **Refused**
 22    How can I see where bar?                       Normal     **Ready**
 20    Why is foo so bar                              Normal     **Started**
 18    No more foo when bar is gone                   Normal     **Talk**
 16    How to get bar from foo                        Normal     **Refused**
 14    Bar cannot baz                                 Normal     **Ready**
 12    Foo cannot bar                                 Normal     **Started**
 10    Where can I find a Foo when bazing Bazes?      Normal     **Talk**
 8     Is there any Bar in Foo?                       Normal     **Refused**
 6     Sell bar in baz                                Normal     **Ready**
 4     Foo and bar don't baz                          Normal     **Started**
 2     Bar is not always baz                          Normal     **Talk**
===== ============================================== ========== ============= ======
<BLANKLINE>


The :class:`TicketsBySite` panel shows all the tickets for a given
site object.  Its default view is a summary:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.TicketsBySite, welket)
... #doctest: -REPORT_UDIFF -SKIP
New : `#97 <Detail>`__, `#73 <Detail>`__, `#49 <Detail>`__, `#25 <Detail>`__, `#1 <Detail>`__
Open : `#115 <Detail>`__, `#91 <Detail>`__, `#67 <Detail>`__, `#43 <Detail>`__, `#19 <Detail>`__

When you open the panel in its own window, you can see the underlying
table:

>>> rt.show(tickets.TicketsBySite, welket, nosummary=True)
... #doctest: -REPORT_UDIFF -SKIP
========== ====================================================================================================== ==========
 Priority   Description                                                                                            Workflow
---------- ------------------------------------------------------------------------------------------------------ ----------
 Normal     `#97 (⛶     'NoneType' object has no attribute 'isocode') <Detail>`__  by *Jean*                       **New**
 Normal     `#73 (⛶     Cannot delete foo) <Detail>`__  by *Jean*                                                  **New**
 Normal     `#49 (⛶     How can I see where bar?) <Detail>`__  by *Jean*                                           **New**
 Normal     `#25 (⛶     'NoneType' object has no attribute 'isocode') <Detail>`__  by *Jean*                       **New**
 Normal     `#1 (⛶ Föö fails to bar when baz) <Detail>`__  by *Jean*                                               **New**
 Normal     `#115 (☉     'NoneType' object has no attribute 'isocode') <Detail>`__  by *Jean*, assigned to *Luc*   **Open**
 Normal     `#91 (☉     Cannot delete foo) <Detail>`__  by *Jean*, assigned to *Luc*                               **Open**
 Normal     `#67 (☉     How can I see where bar?) <Detail>`__  by *Jean*, assigned to *Luc*                        **Open**
 Normal     `#43 (☉     'NoneType' object has no attribute 'isocode') <Detail>`__  by *Jean*, assigned to *Luc*    **Open**
 Normal     `#19 (☉     Cannot delete foo) <Detail>`__  by *Jean*, assigned to *Luc*                               **Open**
========== ====================================================================================================== ==========
<BLANKLINE>

Note that the above table shows no state change actions in the
`Workflow` column.  That's because in this doctest it is being
requested by anonymous. For an authenticated developer it looks like
this:

>>> rt.login('jean').show(tickets.TicketsBySite, welket, nosummary=True)
... #doctest: -REPORT_UDIFF -SKIP
========== ====================================================================================================== ============================================
 Priority   Description                                                                                            Workflow
---------- ------------------------------------------------------------------------------------------------------ --------------------------------------------
 Normal     `#97 (⛶     'NoneType' object has no attribute 'isocode') <Detail>`__                                  [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
 Normal     `#73 (⛶     Cannot delete foo) <Detail>`__                                                             [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
 Normal     `#49 (⛶     How can I see where bar?) <Detail>`__                                                      [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
 Normal     `#25 (⛶     'NoneType' object has no attribute 'isocode') <Detail>`__                                  [✋] [▶] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
 Normal     `#1 (⛶ Föö fails to bar when baz) <Detail>`__                                                          [✋] [■] **New** → [☾] [☎] [☉] [⚒] [☐] [☑]
 Normal     `#115 (☉     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Luc <Detail>`__   [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
 Normal     `#91 (☉     Cannot delete foo) <Detail>`__, assigned to `Luc <Detail>`__                               [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
 Normal     `#67 (☉     How can I see where bar?) <Detail>`__, assigned to `Luc <Detail>`__                        [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
 Normal     `#43 (☉     'NoneType' object has no attribute 'isocode') <Detail>`__, assigned to `Luc <Detail>`__    [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
 Normal     `#19 (☉     Cannot delete foo) <Detail>`__, assigned to `Luc <Detail>`__                               [✋] [▶] **Open** → [☾] [☎] [⚒] [☐] [☑] [☒]
========== ====================================================================================================== ============================================
<BLANKLINE>




Release notes
=============

>>> url = '/choices/deploy/DeploymentsByTicket/milestone'
>>> show_choices('robin', url) #doctest: +SKIP
20150515@welket
20150513@welsch
20150511@welket
20150509@welsch
20150507@welket
20150505@welsch
20150503@welket


>>> show_choices('robin', url+"?query=0507") #doctest: +SKIP
20150507@welket

>>> show_choices('robin', url+"?query=welket") #doctest: +SKIP
20150515@welket
20150511@welket
20150507@welket
20150503@welket

You for meetings you can also seach for digital values and it will return rows that have that number in the name, ref, or remark.
>>> show_choices('robin', url+"?query=2015050") #doctest: +SKIP
20150509@welsch
20150507@welket
20150505@welsch
20150503@welket



Links between tickets
=====================


.. class:: Link
.. class:: Links
.. class:: LinksByTicket
.. class:: LinkType
.. class:: LinkTypes

    The possible values of a :class:`Link`.

    .. attribute:: requires

        The parent ticket requires the child ticket.
    
    .. attribute:: triggers

        The parent ticket triggers the child ticket.
    
    .. attribute:: deploys

        The parent ticket is a deployment which deploys the child ticket.

        Release notes are a printout of a deployment ticket which
        lists the deployed tickets.


>>> rt.show(tickets.LinkTypes)
... #doctest: +REPORT_UDIFF
======= =========== ===========
 value   name        text
------- ----------- -----------
 10      requires    Requires
 20      triggers    Triggers
 30      suggests    Suggests
 40      obsoletes   Obsoletes
======= =========== ===========
<BLANKLINE>




>>> rt.show(tickets.Links)
... #doctest: +REPORT_UDIFF
==== ================= ================================== ==============================
 ID   Dependency type   Parent                             Child
---- ----------------- ---------------------------------- ------------------------------
 1    Requires          #1 (⛶ Föö fails to bar when baz)   #2 (☎ Bar is not always baz)
==== ================= ================================== ==============================
<BLANKLINE>


Comments
========

Comments are not shown to anonymous users:

>>> rt.show(comments.Comments, column_names="id user owner")
==== ================= ================================================================
 ID   Author            Controlled by
---- ----------------- ----------------------------------------------------------------
 1    Jean              `#1 (⛶ Föö fails to bar when baz) <Detail>`__
 2    Luc               `#2 (☎ Bar is not always baz) <Detail>`__
 3    Mathieu           `#3 (☉ Baz sucks) <Detail>`__
 4    Romain Raffault   `#4 (⚒ Foo and bar don't baz) <Detail>`__
 5    Rolf Rompen       `#5 (☾ Cannot create Foo) <Detail>`__
 6    Robin Rood        `#6 (☐ Sell bar in baz) <Detail>`__
 7    Jean              `#7 (☑ No Foo after deleting Bar) <Detail>`__
 8    Luc               `#8 (☒ Is there any Bar in Foo?) <Detail>`__
 9    Mathieu           `#9 (⛶ Foo never matches Bar) <Detail>`__
 10   Romain Raffault   `#10 (☎ Where can I find a Foo when bazing Bazes?) <Detail>`__
 11   Rolf Rompen       `#11 (☉ Class-based Foos and Bars?) <Detail>`__
 12   Robin Rood        `#12 (⚒ Foo cannot bar) <Detail>`__
==== ================= ================================================================
<BLANKLINE>

The same list seen by marc

>>> rt.login('luc').show('comments.Comments', column_names="id user owner")
==== ================= ================================================================
 ID   Author            Controlled by
---- ----------------- ----------------------------------------------------------------
 1    Jean              `#1 (⛶ Föö fails to bar when baz) <Detail>`__
 2    Luc               `#2 (☎ Bar is not always baz) <Detail>`__
 3    Mathieu           `#3 (☉ Baz sucks) <Detail>`__
 4    Romain Raffault   `#4 (⚒ Foo and bar don't baz) <Detail>`__
 5    Rolf Rompen       `#5 (☾ Cannot create Foo) <Detail>`__
 6    Robin Rood        `#6 (☐ Sell bar in baz) <Detail>`__
 7    Jean              `#7 (☑ No Foo after deleting Bar) <Detail>`__
 8    Luc               `#8 (☒ Is there any Bar in Foo?) <Detail>`__
 9    Mathieu           `#9 (⛶ Foo never matches Bar) <Detail>`__
 10   Romain Raffault   `#10 (☎ Where can I find a Foo when bazing Bazes?) <Detail>`__
 11   Rolf Rompen       `#11 (☉ Class-based Foos and Bars?) <Detail>`__
 12   Robin Rood        `#12 (⚒ Foo cannot bar) <Detail>`__
==== ================= ================================================================
<BLANKLINE>


>>> obj = tickets.Ticket.objects.get(pk=2)
>>> rt.login('luc').show(comments.CommentsByRFC, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<p><b>Write comment</b></p><ul><li><a ...>...</a> by <a href="Detail">Luc</a> [<b> Reply </b>] <a ...>⁜</a><div id="comment-2"><p>Very confidential comment</p></div></li></ul>



Filtering tickets
=================

This is a list of the parameters you can use for filterings tickets.

>>> show_fields(tickets.AllTickets, all=True)
+-----------------+-----------------+------------------------------------------------------------------+
| Internal name   | Verbose name    | Help text                                                        |
+=================+=================+==================================================================+
| user            | Author          | The author. The user who reported this ticket to the database    |
|                 |                 | and is responsible for managing it.                              |
+-----------------+-----------------+------------------------------------------------------------------+
| end_user        | End user        | Only rows concerning this end user.                              |
+-----------------+-----------------+------------------------------------------------------------------+
| assigned_to     | Assigned_to     | Only tickets with this user assigned.                            |
+-----------------+-----------------+------------------------------------------------------------------+
| not_assigned_to | Not assigned to | Only that this user is not assigned to.                          |
+-----------------+-----------------+------------------------------------------------------------------+
| interesting_for | Interesting for | Only tickets interesting for this partner.                       |
+-----------------+-----------------+------------------------------------------------------------------+
| site            | Site            | Select a site if you want to see only tickets for this site.     |
+-----------------+-----------------+------------------------------------------------------------------+
| has_site        | Has site        | Show only (or hide) tickets which have a site assigned.          |
+-----------------+-----------------+------------------------------------------------------------------+
| state           | State           | Only rows having this state.                                     |
+-----------------+-----------------+------------------------------------------------------------------+
| priority        | Priority        | Only rows having this priority.                                  |
+-----------------+-----------------+------------------------------------------------------------------+
| show_assigned   | Assigned        | Show only (or hide) tickets that are assigned to somebody.       |
+-----------------+-----------------+------------------------------------------------------------------+
| show_active     | Active          | Show only (or hide) tickets which are active (i.e. state is Talk |
|                 |                 | or ToDo).                                                        |
+-----------------+-----------------+------------------------------------------------------------------+
| show_deployed   | Deployed        | Whether to show tickets with at least one deployment             |
+-----------------+-----------------+------------------------------------------------------------------+
| show_todo       | To do           | Show only (or hide) tickets which are todo (i.e. state is New    |
|                 |                 | or ToDo).                                                        |
+-----------------+-----------------+------------------------------------------------------------------+
| show_private    | Private         | Show only (or hide) tickets that are marked private.             |
+-----------------+-----------------+------------------------------------------------------------------+
| start_date      | Date from       | Start of observed date range                                     |
+-----------------+-----------------+------------------------------------------------------------------+
| end_date        | until           | End of observed date range                                       |
+-----------------+-----------------+------------------------------------------------------------------+
| observed_event  | Observed event  |                                                                  |
+-----------------+-----------------+------------------------------------------------------------------+
| topic           | Topic           |                                                                  |
+-----------------+-----------------+------------------------------------------------------------------+
| has_ref         | Has reference   |                                                                  |
+-----------------+-----------------+------------------------------------------------------------------+



The detail layout of a ticket
=============================

Here is a textual description of the fields and their layout used in
the detail window of a ticket.

>>> from lino.utils.diag import py2rst
>>> print(py2rst(tickets.AllTickets.detail_layout, True))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
(main) [visible for all]:
- **General** (general_1):
  - (general1_1):
    - (general1a):
      - (general1a_1): **Summary** (summary), **ID** (id)
      - (general1a_2): **Site** (site), **Ticket type** (ticket_type)
      - **Workflow** (workflow_buttons)
      - **Description** (description)
    - (general1b):
      - (general1b_1): **Author** (user), **End user** (end_user)
      - (general1b_2): **Assigned to** (assigned_to), **Private** (private)
      - (general1b_3): **Priority** (priority), **Planned time** (planned_time)
      - **Sessions** (working_SessionsByTicket) [visible for consultant hoster developer senior admin]
  - **Comments** (comments_CommentsByRFC) [visible for user consultant hoster developer senior admin]
- **More** (more):
  - (more_1):
    - (more1):
      - (more1_1): **Created** (created), **Modified** (modified), **Fixed since** (fixed_since)
      - (more1_2): **State** (state), **Reference** (ref), **Duplicate of** (duplicate_of), **Deadline** (deadline)
    - **Duplicates** (DuplicatesByTicket)
  - (more_2): **Resolution** (upgrade_notes), **Dependencies** (tickets_LinksByTicket) [visible for senior admin], **Uploads** (uploads_UploadsByController) [visible for user consultant hoster developer senior admin]
<BLANKLINE>



Plugin configuration
====================

    
.. class:: Plugin
           
    See also :class:`lino.core.plugin.Plugin`

    .. attribute:: end_user_model
    .. attribute:: site_model
                   
    .. attribute:: milestone_model

        The model to be used for representing "milestones". Until
        20170331 this was hard-coded to `deploy.Milestone`. Now Lino
        Noi uses `courses.Course`.




Screenshots
===========

.. image:: tickets.Ticket.merge.png
